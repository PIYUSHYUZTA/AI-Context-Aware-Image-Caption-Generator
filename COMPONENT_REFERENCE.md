# Component Reference Guide
## Quick Visual Reference for UI Components

---

## 🎨 Color Swatches

### Primary Colors
```
┌─────────────────┐
│   #fafafa       │  Background Primary (Light Gray)
│   #ffffff       │  Background Secondary (White)
│   #f5f5f5       │  Background Tertiary (Off-White)
└─────────────────┘

┌─────────────────┐
│   #6366f1       │  Accent (Indigo) - Primary Actions
│   #4f46e5       │  Accent Hover (Darker Indigo)
│   #eef2ff       │  Accent Light (Very Light Indigo)
└─────────────────┘

┌─────────────────┐
│   #1a1a1a       │  Text Primary (Near Black)
│   #666666       │  Text Secondary (Medium Gray)
│   #999999       │  Text Tertiary (Light Gray)
└─────────────────┘
```

---

## 📦 Component Anatomy

### Header Component
```
┌────────────────────────────────────────────────────┐
│  [🎨 Icon]  CaptionAI          [ℹ️ About]         │
│             Professional Edition                    │
└────────────────────────────────────────────────────┘
```

**Elements:**
- Logo icon (40x40px, indigo background)
- Title (1.25rem, bold)
- Subtitle (0.75rem, uppercase, gray)
- Action button (right-aligned)

---

### Upload Panel (Left)
```
┌────────────────────────────────────────┐
│  Image Upload                [Step 1]  │
├────────────────────────────────────────┤
│                                        │
│    ┌──────────────────────────┐       │
│    │                          │       │
│    │      [📤 Upload Icon]    │       │
│    │                          │       │
│    │  Drop your image here    │       │
│    │  or click to browse      │       │
│    │                          │       │
│    │  [PNG] [JPG] [JPEG]      │       │
│    │  Maximum file size: 10MB │       │
│    │                          │       │
│    └──────────────────────────┘       │
│                                        │
└────────────────────────────────────────┘
```

**States:**
1. **Empty**: Dashed border, upload instructions
2. **Hover**: Border changes to accent color
3. **Filled**: Shows image preview with remove button

---

### Caption Panel (Right)
```
┌────────────────────────────────────────┐
│  Generated Caption           [Step 2]  │
├────────────────────────────────────────┤
│                                        │
│  ┌──────────────────────────────────┐ │
│  │  [⚡ Generate Caption]           │ │
│  └──────────────────────────────────┘ │
│                                        │
│  ✨ AI GENERATED CAPTION               │
│  ┌──────────────────────────────────┐ │
│  │                                  │ │
│  │  "A beautiful sunset over the    │ │
│  │   ocean with orange and pink     │ │
│  │   colors in the sky"             │ │
│  │                                  │ │
│  └──────────────────────────────────┘ │
│                                        │
│  ┌──────────────────────────────────┐ │
│  │  [📋 Copy to Clipboard]          │ │
│  └──────────────────────────────────┘ │
│                                        │
└────────────────────────────────────────┘
```

**States:**
1. **Empty**: Shows placeholder with instructions
2. **Ready**: Generate button enabled
3. **Loading**: Button shows spinner
4. **Complete**: Caption displayed with copy button

---

### Feature Strip (Bottom)
```
┌──────────────────────────────────────────────────────┐
│  [⚡]  Lightning Fast      [✨]  AI Powered          │
│       Instant AI analysis       Advanced deep        │
│                                  learning            │
│                                                      │
│  [🖼️]  High Accuracy                                │
│       Precise descriptions                           │
└──────────────────────────────────────────────────────┘
```

---

## 🔘 Button Styles

### Primary Button (Generate)
```
┌─────────────────────────────┐
│  [⚡] Generate Caption       │  ← Indigo background
└─────────────────────────────┘     White text
                                    Full width
                                    16px padding
```

### Secondary Button (Copy)
```
┌─────────────────────────────┐
│  [📋] Copy to Clipboard     │  ← Light gray background
└─────────────────────────────┘     Gray text
                                    Border
                                    Full width
```

### Icon Button (Remove)
```
┌───┐
│ ✕ │  ← 32x32px
└───┘     White background
          Gray border
          Hover: Red
```

---

## 📐 Spacing Examples

### Panel Padding
```
┌─────────────────────────────────┐
│ ← 24px →                        │
│                                 │
│  Content Area                   │
│                                 │
│                        ← 24px → │
└─────────────────────────────────┘
```

### Component Gaps
```
[Component 1]
     ↕ 24px gap
[Component 2]
     ↕ 24px gap
[Component 3]
```

---

## 🎭 Interactive States

### Upload Zone States
```
Default:     Border: #e0e0e0 (light gray)
Hover:       Border: #6366f1 (indigo)
             Background: #eef2ff (light indigo)
Active:      Shows image preview
```

### Button States
```
Default:     Background: #6366f1
Hover:       Background: #4f46e5
             Shadow: increased
Active:      Transform: scale(0.98)
Disabled:    Opacity: 0.6
             Cursor: not-allowed
```

---

## 📱 Responsive Breakpoints

### Desktop (1024px+)
```
┌─────────────────────────────────────┐
│           Header                    │
├──────────────┬──────────────────────┤
│   Upload     │    Caption           │
│   Panel      │    Panel             │
└──────────────┴──────────────────────┘
│      Feature Strip (3 columns)      │
└─────────────────────────────────────┘
```

### Tablet (768px - 1023px)
```
┌─────────────────────────────────────┐
│           Header                    │
├─────────────────────────────────────┤
│         Upload Panel                │
├─────────────────────────────────────┤
│         Caption Panel               │
└─────────────────────────────────────┘
│      Feature Strip (1 column)       │
└─────────────────────────────────────┘
```

### Mobile (< 768px)
```
┌──────────────────┐
│  Compact Header  │
├──────────────────┤
│  Upload Panel    │
├──────────────────┤
│  Caption Panel   │
└──────────────────┘
│  Feature Strip   │
└──────────────────┘
```

---

## 🎯 Icon Sizes

```
Small Icons:   16px × 16px  (labels, inline)
Medium Icons:  20px × 20px  (buttons)
Large Icons:   24px × 24px  (features)
XL Icons:      36px × 36px  (upload zone)
XXL Icons:     48px × 48px  (empty states)
```

---

## 📝 Typography Scale

```
Logo Title:      20px (1.25rem)  Bold
Panel Title:     16px (1rem)     Semibold
Upload Title:    18px (1.125rem) Semibold
Caption Text:    18px (1.125rem) Medium
Body Text:       14px (0.875rem) Regular
Small Text:      12px (0.75rem)  Medium
```

---

## 🎨 Background Patterns

### Subtle Grid (Behind Everything)
```
32px × 32px grid
Color: #e0e0e0
Opacity: 0.3
```

### Gradient Overlay
```
Radial gradients at corners
Very subtle indigo tint
Opacity: 0.03
```

---

## ✅ Component Checklist

When implementing each component, ensure:

- [ ] Correct spacing (use CSS variables)
- [ ] Proper border radius
- [ ] Hover states defined
- [ ] Focus states for accessibility
- [ ] Loading states where applicable
- [ ] Error states handled
- [ ] Responsive behavior
- [ ] Icon size consistency
- [ ] Color contrast (WCAG AA)
- [ ] Smooth transitions (0.2s-0.3s)

---

## 🔧 Quick CSS Reference

### Common Patterns

**Panel Container:**
```css
background: var(--color-bg-secondary);
border: 1px solid var(--color-border);
border-radius: var(--radius-lg);
box-shadow: var(--shadow-sm);
```

**Primary Button:**
```css
background: var(--color-accent);
color: white;
padding: var(--space-4) var(--space-6);
border-radius: var(--radius-md);
font-weight: 600;
```

**Badge/Tag:**
```css
padding: var(--space-1) var(--space-3);
background: var(--color-accent-light);
color: var(--color-accent);
border-radius: var(--radius-full);
font-size: 0.75rem;
text-transform: uppercase;
```

---

## 🎯 Quick Tips

1. **Always use CSS variables** for colors and spacing
2. **Maintain consistent icon sizes** (16, 20, 24, 36, 48)
3. **Add hover states** to all interactive elements
4. **Use subtle shadows** for depth (don't overdo it)
5. **Keep borders light** (#e0e0e0 is your friend)
6. **Generous whitespace** prevents clutter
7. **Test on mobile** early and often
8. **Smooth transitions** make it feel polished

---

This reference guide provides quick visual patterns for implementing the professional UI design. Use it alongside the main UI_DESIGN_GUIDE.md for complete implementation details.
