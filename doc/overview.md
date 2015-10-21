# Project Overview

This document includes a general overview of the project and its main packages,
including a list of their models and a short explanation of their core
functionality.

The project is split in six (6) packages:

+ common
+ accounts
+ geo
+ organizations
+ resources
+ work
+ deployment


## common

This package is not a django app, but a group of common functionality shared
among different apps, such as base classes, helper functions, etc.

### Models

+ OwnedEntity: base model for all entities that are not global
+ History: base class for transition history data

### Query

+ OwnedEntityQuerySet: base queryset for all collections that are not global


## accounts

This package contains the models related to accounts and their users.

### Models:

+ Account: entity that represents a client (owner of its data)
+ UserProfile: extra information for user, especially related to the account


## geo

App that contains the models that represent geographical entities.

### Models

+ Nation: main geographical entity
+ Region: highest-level administrative division, such as province or state
+ Locality: lowest-level administrative division, such as city or town
+ Location: specific spot with a unique address, such as building or complex
+ Space: lodging or storage area used to track resource location


## organizations

App that contains the organizational entities.

### Models

+ Company: organization to which projects and resources are assigned
+ Team: group of resources performing related activities

### Query

+ OwnedEntityQuerySet: base queryset for all collections that are not global


## resources

App that contains the models that represent durable resources, such as machinery
or employees.

### Models

+ Position: employee positions from which a user can choose
+ EquipmentType: group to classify equipment
+ Resource: base model with common data among employee and equipment
+ Employee: person that performs activities
+ Equipment: machine/device used to perform activities
+ LocationHistory: historical assignment of resources to location
+ SpaceHistory: historical assignment of resources to spaces
+ CompanyHistory: historical assignment of resources to companies
+ TeamHistory: historical assignment of resources to teams
+ ProjectHistory: historical assignment of resources to projects
+ PositionHistory: historical assignment of employees to positions


## work

App that contains the work definition, such as scope, WBS and related entities.

### Models

+ Project: main unit of work with a specific scope
+ ActivityGroupType: type of group
+ ActivityGroup: entity to group activities outside structure (phase, discpline)
+ Activity: component of hierarchical scope definition in a project


## deployment

App that joins the resources and work.

### Models:

+ TimeSheet: tracks daily work of a team
+ WorkLog: tracks hours spent by resources in specific activities

