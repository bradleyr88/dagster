---
description: Example use cases for customizing `AutomationCondition.on_cron()`
sidebar_position: 100
title: Customizing `AutomationCondition.on_cron()`
---

### Updating older time partitions

By default, `AutomationCondition.on_cron()` will target the latest time partition of an asset.

If you instead want to update partitions on a delay, then you can replace this condition with one that targets a partition that has a specific lag from the latest time window:

<CodeExample path="docs_snippets/docs_snippets/concepts/declarative_automation/on_cron/update_specific_older_partition.py" />

## Ignoring dependencies

By default, `AutomationCondition.on_cron()` will wait for all upstream dependencies to be updated before executing the asset it's attached to. In some cases, it can be useful to ignore some upstream dependencies in this calculation. This can be done by passing in an <PyObject section="assets" module="dagster" object="AssetSelection" /> to be ignored:

<CodeExample path="docs_snippets/docs_snippets/concepts/declarative_automation/on_cron/ignore_dependencies_cron.py" />

Alternatively, you can pass in an <PyObject section="assets" module="dagster" object="AssetSelection" /> to be allowed:

<CodeExample path="docs_snippets/docs_snippets/concepts/declarative_automation/on_cron/allow_dependencies_cron.py" />