---
description: Example use cases for customizing `AutomationCondition.eager()`
sidebar_position: 300
title: Customizing `AutomationCondition.eager()`
---


### Ignoring missing upstream data

By default, `AutomationCondition.eager()` will not materialize a target if it has any missing upstream data.

If it is expected to have missing upstream data, remove `~AutomationCondition.any_deps_missing()` from the eager policy to allow execution:

<CodeExample path="docs_snippets/docs_snippets/concepts/declarative_automation/eager/allow_missing_upstreams.py" />

### Updating older time partitions

By default, `AutomationCondition.eager()` will only update the latest time partition of an asset.

If updates to historical partitions should result in downstream updates, then this sub-condition can be removed:

<CodeExample path="docs_snippets/docs_snippets/concepts/declarative_automation/eager/update_older_time_partitions.py" />

## Waiting for all blocking asset checks to complete before executing

The `AutomationCondition.all_deps_blocking_checks_passed()` condition becomes true after all upstream blocking checks have passed.

This can be combined with `AutomationCondition.eager()` to ensure that your asset does not execute if upstream data is failing data quality checks:

<CodeExample path="docs_snippets/docs_snippets/concepts/declarative_automation/eager/blocking_checks_condition.py" />

## Ignoring runs from non-automated runs when using AutomationCondition.eager()

By default, `AutomationCondition.eager()` materializes a target whenever any upstream event occurs, regardless of the source of that event.

It can be useful to ignore runs of certain types when determining if an upstream asset should be considered "updated". This can be done using `AutomationCondition.executed_with_tags()` to filter updates for runs with tags matching particular keys:

<CodeExample path="docs_snippets/docs_snippets/concepts/declarative_automation/eager/executed_with_tags_condition.py" />
