# Nix-Lock

*A delayed deployment workflow for NixOS.*

## What is Nix-Lock?

Most update workflows answer the question:

> **“What is the latest version available?”**

Nix-Lock answers a different question:

> **“Which previously captured operating system has completed its observation period?”**

Rather than immediately deploying every newly built NixOS system, Nix-Lock separates the act of building a system from the act of deploying it.

A candidate system is built once, preserved unchanged, allowed to complete an observation period, and intentionally deployed later.

The result is a release management workflow that separates **candidate capture** from **deployment** while preserving the normal NixOS administration experience.

## Why?

New software releases occasionally introduce regressions, incompatibilities, or unexpected behaviour.

Many users respond by waiting before updating. However, waiting manually usually means installing whatever revision happens to be current when the waiting period ends.

That is not the same as allowing one specific revision to complete an observation period.

Nix-Lock solves this by building and preserving an exact immutable NixOS system closure at a chosen point in time.

That same closure can then be deployed later, regardless of how the available configuration or package sources have changed in the meantime.

The goal is not to avoid updates.

The goal is to make deployment intentional.

## How It Works

The workflow is deliberately simple:

```text
Capture → Observe → Deploy → Repeat
```

1. Build the current NixOS configuration without activating it.
2. Preserve the resulting immutable system closure.
3. Continue using and maintaining the computer normally.
4. Allow the candidate to complete its observation period unchanged.
5. Deploy that exact candidate.
6. Capture the next candidate.

Personal files, documents, development work, and ordinary system use continue normally.

Only the timing of operating system deployment changes.

The observation period is a matter of deployment policy. Nix-Lock does not attempt to decide how long a candidate should be retained before deployment.

## Usage

Enter the Nix-Lock development environment:

```bash
cd ~/Nix-lock
nix-shell
```

The current command interface is:

```text
python3 nix_lock.py {capture|status|deploy}
```

### Capture

```bash
python3 nix_lock.py capture
```

`capture` builds the current NixOS configuration without activating it.

The resulting system closure is validated and retained using Nix-Lock's persistent garbage-collection root.

If an earlier candidate exists, Nix-Lock protects the new candidate before releasing its own reference to the previous candidate.

### Status

```bash
python3 nix_lock.py status
```

`status` reports the currently retained candidate and verifies:

* the store path is present
* garbage-collection protection is present
* the candidate contains a valid NixOS system activation program

### Deploy

```bash
python3 nix_lock.py deploy
```

`deploy` activates the exact retained candidate.

It does not rebuild the current configuration or attempt to reproduce the candidate from current package sources.

After deployment, Nix-Lock verifies that `/run/current-system` resolves to the retained candidate closure.

A new candidate can then be captured for the next observation cycle.

## Architecture

Nix-Lock does not maintain its own archive of operating systems.

Nix already stores immutable system closures and already provides the mechanisms required to protect and activate them.

Nix-Lock therefore owns one persistent garbage-collection root:

```text
~/.local/state/nix-lock/candidate
```

That root:

* identifies the retained candidate
* protects the candidate from garbage collection
* provides a stable location from which the candidate can be inspected

Nix continues to own storage, closure identity, activation, and garbage collection.

Nix-Lock adds policy around when an already-built closure should be deployed.

## Project Goals

Nix-Lock aims to:

* Build immutable NixOS deployment candidates.
* Preserve candidates unchanged.
* Separate build time from deployment time.
* Allow observation periods to be determined by deployment policy.
* Deploy previously built system closures.
* Preserve reproducibility.
* Integrate with existing NixOS workflows.
* Minimise operational complexity.

## Non-Goals

Nix-Lock is **not** intended to:

* Replace NixOS generations.
* Replace backups.
* Snapshot user data.
* Restore complete machine state.
* Predict whether updates are safe.
* Test packages.
* Replace Git.
* Replace existing NixOS tooling.
* Require Home Manager.
* Require users to redesign an existing NixOS configuration.

## Current Status

Nix-Lock has completed its first full experimental deployment cycle.

The proof of concept can:

* build a NixOS system without activating it
* identify the resulting immutable system closure
* preserve that closure using a persistent garbage-collection root
* verify that the retained closure is a valid NixOS system
* report the currently retained candidate
* safely replace an earlier candidate
* deploy the exact retained closure without rebuilding it
* verify that the deployed closure became `/run/current-system`

The first complete real-world cycle began with a candidate captured on August 1, 2026:

```text
/nix/store/hg414yf21h392z8ik8yb1x1n29szak2w-nixos-system-nixos-26.05.6200.8623c4c20aa4
```

The candidate was retained while the computer continued through almost four weeks of ordinary use, system changes, rebuilds, and maintenance.

At the end of the observation period, Nix-Lock confirmed that:

```text
Store path: present
GC protection: present
NixOS system closure: valid
```

The candidate was then deployed directly from the preserved closure.

After deployment:

```text
/run/current-system
```

resolved to the exact closure captured at the beginning of the observation period.

No reconstruction of the candidate from the current configuration or current package sources was required.

This completed the first demonstrated:

```text
Capture → Observe → Deploy
```

cycle.

A new candidate has subsequently been captured and retained, beginning the next observation cycle.

The central mechanism of Nix-Lock has therefore moved from hypothesis to demonstrated behaviour.

## Development Approach

Nix-Lock is being developed experimentally.

Assumptions are tested before additional abstraction or automation is introduced.

Failed approaches are documented rather than removed from the project history because they explain how the current design was reached and may help others avoid repeating the same investigation.

The project should remain as small as its purpose allows.

Where Nix already provides the required mechanism, Nix-Lock should use it rather than replace it.

Implementation should follow demonstrated need rather than anticipated complexity.

## Documentation

The project documentation records:

* the original problem
* rejected approaches
* experimental findings
* architectural decisions
* current implementation
* demonstrated behaviour
* remaining questions and possible future work

It is the authoritative description of the project's intended behaviour and the reasoning behind its design.

## Contributing

Ideas, experiments, corrections, and constructive feedback are welcome.

Alternative approaches are particularly useful when they are accompanied by an explanation of what was tested and what was observed.

The project deliberately favours simplicity over features.

Proposed changes should support the central aim of separating system capture from system deployment without unnecessarily increasing operational complexity.

## License

This project is released under the MIT License.

-- Oggie --

