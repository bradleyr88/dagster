---
description: Dagster Declarative Automation is a framework that allows you to access information about events that impact the status of your assets, and the dependencies between them.
keywords:
- declarative
- automation
- schedule
- automation condition
sidebar_position: 20
title: Declarative Automation
---

Declarative Automation is a framework that uses information about the status of your assets and their dependencies to launch executions of your assets.

Not sure what automation method to use? Check out the [automation overview](../automation-overview/) for a comparison of the different automation methods available in Dagster.

::: note

In order to enable Declarative Automation, you will need to:

- Set an **[automation condition](#automation-conditions)** on an asset or asset check, which represents when an individual asset or check should be executed.
- Enable the default **[automation condition sensor](#automation-condition-sensors)** in the UI, which evaluates automation conditions and launches runs in response to their statuses.
  1. Navigate to **Automation**.
  2. Locate the desired code location.
  3. Toggle on the **default_automation_condition_sensor** sensor.

:::

## Automation conditions

An <PyObject section="assets" module="dagster" object="AutomationCondition" /> on an asset or asset check describe the conditions under which work should be executed.

The system is extremely flexible, and can be customized to fit your specific needs, but it is recommended to start with one of the built-in conditions and customize it from there, rather than building up your own condition from scratch.

### `AutomationCondition.on_cron()`: Executing on a schedule after dependencies

::: note

Learn how to customize this automation condition in the [Customizing AutomationCondition.on_cron()](customizing-automation-conditions/#customizing-automationconditionon_cron) section.

:::

Assets often need to execute on a regular cadence, but only *after* their upstream dependencies have been materialized. The <PyObject section="assets" module="dagster" object="AutomationCondition.on_cron" /> condition allows you to specify a cron schedule for when the asset should be executed, while also ensuring that it only runs after its upstream dependencies have been materialized during that time period.

This allows you to create a schedule for each asset that is independent of the specifics of how your upstream data is automated, while still ensuring that the asset is only executed when it has the data it needs.

#### Example

<CodeExample path="docs_snippets/docs_snippets/concepts/declarative_automation/on_cron/basic.py" />

At the start of each hour, the above asset will start waiting for each of its dependencies to be updated. Once all dependencies have updated since the start of the hour, this asset will be immediately kicked off.


### `AutomationCondition.on_missing()`: Executing time-partitioned assets as soon as upstream data is available

::: note

Learn how to customize this automation condition in the [Customizing AutomationCondition.on_missing()](customizing-automation-conditions/#customizing-automationconditionon_missing) section.

:::

When assets are partitioned by a time dimension, new partitions will continually appear as time passes. The <PyObject section="assets" module="dagster" object="AutomationCondition.on_missing" /> condition allows you to materialize these partitions as soon as all upstream partitions are filled in.

This allows you to easily manage dependencies between partitioned assets, such as hourly-partitioned assets downstream of daily-partitioned ones.

#### Example

<CodeExample path="docs_snippets/docs_snippets/concepts/declarative_automation/on_missing/basic.py" />

As soon as all hourly partitions of the upstream asset are filled in, the downstream asset will be immediately kicked off.
  

### `AutomationCondition.eager()`: Executing when upstream assets are updated

::: note

Learn how to customize this automation condition in the [Customizing AutomationCondition.eager()](customizing-automation-conditions/#customizing-automationconditioneager) section.

:::

The <PyObject section="assets" module="dagster" object="AutomationCondition.eager" /> condition allows you to automatically update an asset whenever any of its dependencies are updated. 

#### Example

<CodeExample path="docs_snippets/docs_snippets/concepts/declarative_automation/eager/basic.py" />

The above asset will be automatically updated whenever any of its upstream dependencies are updated. This is useful for assets that are not time-partitioned, or when you want to ensure that the latest data is always available.