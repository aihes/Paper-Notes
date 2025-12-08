# Cline CLI Command Summary

This document provides a comprehensive summary of the Cline CLI commands, based on the official documentation.

## Global Options

These options apply to all subcommands:

-   `-F, --output-format format`: Output format. Options: `rich` (default), `json`, `plain`.
-   `-h, --help`: Display help information for the command.
-   `-v, --verbose`: Enable verbose output for debugging.

## Instant Task Mode

The simplest way to use Cline. It immediately spawns an instance, creates a task, and enters chat mode.

**Syntax:** `cline "prompt here" [options]`

**Options:**

-   `-o, --oneshot`: Cline completes the task and stops.
-   `-s, --setting setting value`: Override a setting for this task.
-   `-y, --no-interactive, --yolo`: Enable fully autonomous mode.
-   `-m, --mode mode`: Starting mode. Options: `act` (default), `plan`.

---

## Main Commands

### Authentication (`auth` / `a`)

Configure authentication for AI model providers.

**Usage:**

-   `cline auth`: Launches an interactive wizard.
-   `cline auth [provider]`: Prompts for the key or starts OAuth flow.
-   `cline auth [provider] [key]`: Directly configures the provider with the given key.

---

### Instance Management (`instance` / `i`)

Manage Cline Core instances, which are independent agent processes.

**Subcommands:**

-   `cline instance new` or `cline i n`:
    -   **Description:** Spawns a new Cline Core instance.
    -   **Flags:**
        -   `-d, --default`: Sets the new instance as the default.

-   `cline instance list` or `cline i l`:
    -   **Description:** Lists all running Cline Core instances.

-   `cline instance default <address>` or `cline i d <address>`:
    -   **Description:** Sets a default instance for future commands.

-   `cline instance kill <address>` or `cline i k <address>`:
    -   **Description:** Terminates a specific Cline Core instance.
    -   **Flags:**
        -   `-a, --all`: Kills all running instances.

---

### Task Management (`task` / `t`)

Manage tasks, which represent individual work items for Cline.

**Global Task Flag:**

-   `-a, --address ADDR`: Specifies the Cline Core instance to use (e.g., `localhost:50052`).

**Subcommands:**

-   `cline task new <prompt> [options]` or `cline t n <prompt> [options]`:
    -   **Description:** Creates a new task.
    -   **Options:**
        -   `-s, --setting setting value`: Sets task-specific settings.
        -   `-y, --no-interactive, --yolo`: Enables autonomous mode.
        -   `-m, --mode mode`: Sets the starting mode (`act` or `plan`).

-   `cline task open <task-id> [options]` or `cline t o <task-id> [options]`:
    -   **Description:** Resumes a previous task from history.

-   `cline task list` or `cline t l`:
    -   **Description:** Lists all tasks in history.

-   `cline task chat` or `cline t c`:
    -   **Description:** Enters interactive chat mode for the current task.

-   `cline task send [message] [options]` or `cline t s [message] [options]`:
    -   **Description:** Sends a message to Cline. Reads from stdin if no message is provided.
    -   **Options:**
        -   `-a, --approve`: Approves Cline's proposed action.
        -   `-d, --deny`: Denies Cline's proposed action.
        -   `-f, --file FILE`: Attaches a file to the message.

-   `cline task view [options]` or `cline t v [options]`:
    -   **Description:** Displays the current conversation.
    -   **Options:**
        -   `-f, --follow`: Streams updates in real-time.
        -   `-c, --follow-complete`: Follows until the task is completed.

-   `cline task restore <checkpoint>` or `cline t r <checkpoint>`:
    -   **Description:** Restores a task to a previous checkpoint.

-   `cline task pause` or `cline t p`:
    -   **Description:** Pauses task execution.

---

### Configuration (`config` / `c`)

Manage global configuration settings.

**Subcommands:**

-   `cline config set <key> <value>` or `cline c s <key> <value>`:
    -   **Description:** Sets a configuration variable.

-   `cline config get <key>` or `cline c g <key>`:
    -   **Description:** Reads a configuration variable.

-   `cline config list` or `cline c l`:
    -   **Description:** Lists all configuration variables and their values.

---

## Other Commands

-   `cline completion <shell>`: Generates autocompletion scripts for `bash`, `zsh`, `fish`, or `powershell`.
-   `cline version`: Displays the installed Cline CLI version.