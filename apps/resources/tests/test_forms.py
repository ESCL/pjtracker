from datetime import date

from django.test import TestCase
from django.contrib.auth.models import Group

from ...accounts.factories import UserFakeFactory
from ...deployment.factories import ResourceProjectAssignmentFakeFactory
from ...deployment.models import ResourceProjectAssignment, ResourceProjectAssignmentAction
from ...resources.factories import EmployeeFakeFactory
from ...work.factories import ProjectFakeFactory
from ..forms import ResourceProjectAssignmentForm, ResourceProjectAssignmentActionForm


class ResourceProjectAssignmentFormTest(TestCase):

    def setUp(self):
        # Create project and resource
        self.employee = EmployeeFakeFactory.create()
        self.pj = ProjectFakeFactory.create(owner=self.employee.owner)

        # Create user with HR group
        self.user = UserFakeFactory.create(owner=self.employee.owner,
                                           groups=[Group.objects.get(name='Human Resources')])

    def test_validate(self):
        # New instance with fields missing, fail
        data = {}
        form = ResourceProjectAssignmentForm(data, parent=self.employee.resource_ptr, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertEqual(set(form.errors.keys()), {'project', 'start_date'})

        # No end date, OK
        data = {'project': self.pj.id, 'start_date': date(2016, 1, 10)}
        form = ResourceProjectAssignmentForm(data, parent=self.employee.resource_ptr, user=self.user)
        self.assertTrue(form.is_valid())

        # Bad end date, fail
        data['end_date'] = date(2016, 1, 9)
        form = ResourceProjectAssignmentForm(data, parent=self.employee.resource_ptr, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertEqual(set(form.errors.keys()), {'end_date'})

        # Correct end date, OK
        data['end_date'] = date(2017, 1, 9)
        form = ResourceProjectAssignmentForm(data, parent=self.employee.resource_ptr, user=self.user)
        self.assertTrue(form.is_valid())

        # Create an issued, colliding assignment, should fail now
        self.assignment = ResourceProjectAssignmentFakeFactory.create(
            owner=self.employee.owner, resource=self.employee.resource_ptr,
            status=ResourceProjectAssignment.STATUS_ISSUED,
            start_date=date(2015, 12, 20)
        )
        form = ResourceProjectAssignmentForm(data, parent=self.employee.resource_ptr, user=self.user)
        self.assertFalse(form.is_valid())

    def test_save(self):
        # Save form, make sure it saves resource
        data = {'project': self.pj.id, 'start_date': date(2016, 1, 10)}
        form = ResourceProjectAssignmentForm(data, parent=self.employee.resource_ptr, user=self.user)
        form.is_valid()
        pa = form.save()
        self.assertEqual(pa.project, self.pj)
        self.assertEqual(pa.resource.instance, self.employee)


class ResourceProjectAssignmentActionFormTest(TestCase):

    def setUp(self):
        # Create project, resource and assignment
        self.employee = EmployeeFakeFactory.create()
        self.pj = ProjectFakeFactory.create(owner=self.employee.owner)
        self.assignment = ResourceProjectAssignmentFakeFactory.create(
            owner=self.employee.owner, resource=self.employee.resource_ptr
        )

        # Create users with permissions
        self.user = UserFakeFactory.create(owner=self.employee.owner,
                                           groups=[Group.objects.get(name='Human Resources')])
        self.boss = UserFakeFactory.create(owner=self.employee.owner,
                                           groups=[Group.objects.get(name='Project Management')])

    def test_init(self):
        # Pending assignment, should allow only Issue
        form = ResourceProjectAssignmentActionForm(user=self.user, instance=self.assignment)
        self.assertEqual(form.fields['action'].choices, [('issue', 'Issue')])

        # Issued assignment, allows review (reject, approve)
        self.assignment.status = ResourceProjectAssignment.STATUS_ISSUED
        form = ResourceProjectAssignmentActionForm(user=self.user, instance=self.assignment)
        self.assertEqual(form.fields['action'].choices, [('approve', 'Approve'), ('reject', 'Reject')])

    def test_clean(self):
        # Approve when pending, invalid option
        self.assignment.status = ResourceProjectAssignment.STATUS_PENDING
        data = {'action': 'approve'}
        form = ResourceProjectAssignmentActionForm(data, user=self.user, instance=self.assignment)
        self.assertFalse(form.is_valid())
        self.assertEqual(set(form.errors.keys()), {'action'})

        # Issue assignment and approve, OK
        self.assignment.status = ResourceProjectAssignment.STATUS_ISSUED
        form = ResourceProjectAssignmentActionForm(data, user=self.user, instance=self.assignment)
        self.assertTrue(form.is_valid())

        # Now reject w/o feedback
        data['action'] = 'reject'
        form = ResourceProjectAssignmentActionForm(data, user=self.user, instance=self.assignment)
        self.assertFalse(form.is_valid())
        self.assertEqual(set(form.errors.keys()), {'feedback'})

        # Reject w/ feedback, OK
        data['feedback'] = 'That is wrong.'
        form = ResourceProjectAssignmentActionForm(data, user=self.user, instance=self.assignment)
        self.assertTrue(form.is_valid())

        # Create an issued, colliding assignment
        ResourceProjectAssignmentFakeFactory.create(
            owner=self.employee.owner, resource=self.employee.resource_ptr,
            status=ResourceProjectAssignment.STATUS_ISSUED,
            start_date=date(2015, 12, 20)
        )

        # Reject w/ feedback, OK even with collision
        form = ResourceProjectAssignmentActionForm(data, user=self.user, instance=self.assignment)
        self.assertTrue(form.is_valid())

        # Not allowed to approve due to collision
        data['action'] = 'approve'
        form = ResourceProjectAssignmentActionForm(data, user=self.user, instance=self.assignment)
        self.assertFalse(form.is_valid())

    def test_save(self):
        # Issue assignment, should update status and add action instance
        data = {'action': 'issue'}
        form = ResourceProjectAssignmentActionForm(data, user=self.user, instance=self.assignment)
        form.is_valid()
        form.save()
        self.assignment.refresh_from_db()
        self.assertEqual(self.assignment.status, ResourceProjectAssignment.STATUS_ISSUED)
        self.assertEqual(self.assignment.actions.count(), 1)
        a = self.assignment.actions.get()
        self.assertEqual(a.action, ResourceProjectAssignmentAction.ISSUED)
        self.assertEqual(a.actor, self.user)

        # Reject assignment
        data = {'action': 'reject', 'feedback': 'wrong.'}
        form = ResourceProjectAssignmentActionForm(data, user=self.boss, instance=self.assignment)
        form.is_valid()
        form.save()
        self.assignment.refresh_from_db()
        self.assertEqual(self.assignment.status, ResourceProjectAssignment.STATUS_REJECTED)
        self.assertEqual(self.assignment.actions.count(), 2)
        a = self.assignment.actions.last()
        self.assertEqual(a.action, ResourceProjectAssignmentAction.REJECTED)
        self.assertEqual(a.actor, self.boss)

        # Issue again
        data = {'action': 'issue'}
        form = ResourceProjectAssignmentActionForm(data, user=self.user, instance=self.assignment)
        form.is_valid()
        form.save()
        self.assignment.refresh_from_db()
        self.assertEqual(self.assignment.status, ResourceProjectAssignment.STATUS_ISSUED)
        self.assertEqual(self.assignment.actions.count(), 3)
        a = self.assignment.actions.last()
        self.assertEqual(a.action, ResourceProjectAssignmentAction.ISSUED)
        self.assertEqual(a.actor, self.user)

        # Approve assignment
        data = {'action': 'approve', 'feedback': 'ok now.'}
        form = ResourceProjectAssignmentActionForm(data, user=self.boss, instance=self.assignment)
        form.is_valid()
        form.save()
        self.assignment.refresh_from_db()
        self.assertEqual(self.assignment.status, ResourceProjectAssignment.STATUS_APPROVED)
        self.assertEqual(self.assignment.actions.count(), 4)
        a = self.assignment.actions.last()
        self.assertEqual(a.action, ResourceProjectAssignmentAction.APPROVED)
        self.assertEqual(a.actor, self.boss)
