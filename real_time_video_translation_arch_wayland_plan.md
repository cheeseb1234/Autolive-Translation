# Real-Time Video Text Translation — Arch Linux / Wayland-First Development Plan

> Purpose: This file is a clean Markdown handoff for Claude or another coding assistant. It summarizes the intended architecture, platform assumptions, module plan, and Codex-style implementation milestones for an open-source real-time text-in-video translation project.

You’re right: **for a new Arch Linux project, Wayland should be the primary target**.

I only suggested X11 because it is the easier prototype path: unrestricted screen capture, easier transparent overlays, fewer compositor security boundaries. But for the project you’re describing, especially if it is meant to become a useful open-source tool, **X11 should be treated as a fallback/debug backend, not the main path**.

Wayland is clearly where the Linux desktop is going. KDE has announced that Plasma 6.8 will be Wayland-exclusive for the Plasma session, while X11 apps continue through Xwayland; KDE also says Wayland is already the default on most distributions. GNOME has also been moving away from its X11 session, with GDM disabling the X11 session by default as part of deprecating it. ([blogs.kde.org](https://blogs.kde.org/2025/11/26/going-all-in-on-a-wayland-future/))

So the revised answer is:

```text
Primary target: Wayland
Compatibility/debug target: X11
Do not build the architecture around X11.
```

# Why keep X11 at all?

Only for three practical reasons:

1. **Debugging the pipeline faster**  
   X11 makes it easier to prove OCR, tracking, translation, and overlay logic before fighting Wayland permissions.

2. **Fallback for unusual setups**  
   Some users, older desktops, remote sessions, and edge cases may still run X11.

3. **Simpler CI/dev testing**  
   It is easier to fake or automate some X11 workflows than full Wayland portal/compositor behavior.

But those are engineering conveniences, not the product direction.

# Better development plan

The project should be **Wayland-first**, with this order:

```text
1. Replay provider
2. Wayland PipeWire portal capture
3. Subtitle-band overlay fallback
4. OCR / translation / tracking
5. Wayland layer-shell overlay
6. Optional X11 capture/overlay fallback
```

That avoids wasting time building a polished X11 version that will age poorly.

# Revised module plan

## Capture

Primary:

```text
PipeWire + xdg-desktop-portal ScreenCast
```

The portal ScreenCast API is the correct Wayland-native path. It creates screen-cast sessions, lets the user select monitor/window sources, and returns PipeWire stream information for frame access. ([flatpak.github.io](https://flatpak.github.io/xdg-desktop-portal/docs/doc-org.freedesktop.portal.ScreenCast.html))

Module layout:

```text
src/rtt/capture/
  base.py
  replay.py
  pipewire_portal.py
  x11_mss.py       # fallback only
```

Codex instruction:

```text
Implement Wayland capture first using xdg-desktop-portal ScreenCast + PipeWire.
Keep X11 MSS capture as an optional fallback backend, not the default.
```

---

## Overlay

Primary fallback:

```text
Subtitle band window
```

Primary advanced overlay:

```text
Wayland layer-shell overlay
```

Wayland intentionally does not allow arbitrary global overlays the way X11 does. That means a normal PySide transparent always-on-top window is not the right assumption. The realistic Wayland path is:

```text
simple subtitle-band overlay first
→ compositor-specific layer-shell overlay later
```

Module layout:

```text
src/rtt/overlay/
  base.py
  subtitle_band.py
  gtk_layer_shell.py
  x11_pyside.py       # fallback only
```

Codex instruction:

```text
Implement SubtitleBandOverlayRenderer first because it works across more Wayland desktops.
Then implement GtkLayerShellOverlayRenderer for wlroots/Hyprland/Sway-style compositors.
Do not rely on X11-style always-on-top behavior.
```

---

## Platform detector

This becomes important:

```text
src/rtt/platform/linux_env.py
```

It should detect:

```text
Wayland or X11
compositor hints
PipeWire availability
xdg-desktop-portal availability
portal backend
layer-shell availability
OCR engines
translation engines
```

Codex instruction:

```text
Make rtt doctor explain whether the user can run the Wayland path.
Do not silently fall back to X11 unless the user asks.
```

---

# Updated MVP for Arch

The MVP should now be:

```text
Replay frames
→ OCR
→ translation
→ subtitle-band overlay
```

Then:

```text
Wayland PipeWire capture
→ OCR
→ text tracking
→ Argos Translate
→ subtitle-band overlay
```

Then:

```text
Wayland layer-shell in-place overlay
```

X11 comes later as:

```text
Optional fallback:
MSS capture + PySide6 overlay
```

# Updated Codex milestone order

## PR 1 — Core skeleton

```text
Create project skeleton, core dataclasses, config loader, CLI, and rtt doctor.
Make Linux/Wayland the default platform assumption.
Stub capture, OCR, translation, tracking, and overlay interfaces.
```

## PR 2 — Replay pipeline

```text
Implement ReplayCaptureProvider.
Allow the whole OCR/translation/overlay pipeline to run from screenshots or sample frames.
This avoids blocking the project on PipeWire capture.
```

## PR 3 — Subtitle-band overlay

```text
Implement a Wayland-safe SubtitleBandOverlayRenderer.
It should be a normal window that displays active translated tracks as subtitles.
Do not attempt global transparent overlay yet.
```

## PR 4 — OCR and translation

```text
Implement PaddleOCRProvider, RapidOCRProvider stub, and ArgosTranslator.
Add SQLite cache.
```

## PR 5 — Wayland capture

```text
Implement PipeWirePortalCaptureProvider using xdg-desktop-portal ScreenCast.
The provider should request monitor/window capture, receive the PipeWire stream node, and emit FramePacket objects.
```

## PR 6 — Tracking

```text
Implement IoU text tracking, stability voting, translation-on-change, and cache reuse.
```

## PR 7 — Layer-shell overlay

```text
Implement GtkLayerShellOverlayRenderer for Wayland compositors that support layer-shell.
Use it for in-place translated text overlay.
Fallback to subtitle-band mode when unavailable.
```

## PR 8 — X11 fallback

```text
Add optional MSSX11CaptureProvider and PySideX11OverlayRenderer.
Mark them as fallback/debug backends.
```

# Bottom line

You probably **shouldn’t bother with X11 as a first-class target**.

For this project:

```text
Wayland-first: yes
X11-supported: optional
X11-designed-around: no
```

The smart compromise is: use replay files to debug the pipeline, not X11. That gives you the same “easy development” benefit without anchoring the architecture to old Linux display behavior.


---

# Claude Implementation Prompt

You are helping build an open-source Arch Linux-first real-time screen text translation app.

## Product goal

Create a modular, Wayland-first desktop application that captures video/screen frames, detects visible text, OCRs it, stabilizes text across frames, translates stable text offline, caches OCR/translation results, and displays translated text using a Wayland-safe overlay strategy.

## Platform assumptions

- Primary platform: Arch Linux on Wayland.
- X11 is optional fallback/debug support only.
- Do not design the app around X11 assumptions.
- Use replay fixtures to develop and test the pipeline before live capture is complete.
- Wayland capture should use xdg-desktop-portal ScreenCast and PipeWire.
- Wayland overlay should start with a subtitle-band fallback, then add layer-shell for advanced in-place overlays.

## Core pipeline

```text
capture frame
→ detect/choose regions of interest
→ OCR text
→ group text boxes into translation units
→ track text over time
→ stabilize text
→ translate only stable changed text
→ cache OCR and translation results
→ render translated output
```

## First implementation target

Start with:

```text
ReplayCaptureProvider
→ OCR provider stub / later PaddleOCR
→ translation provider stub / later Argos Translate
→ SQLite cache
→ SubtitleBandOverlayRenderer
→ CLI + rtt doctor
```

Do not begin with deep inpainting, perfect text replacement, or X11-specific overlay behavior. Prioritize a working, testable, modular Wayland-first pipeline.
