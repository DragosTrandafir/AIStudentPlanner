# Data Model Relationships & Cascade Behavior

This document explains the non-trivial relationships between entities, cascade delete behavior, and cross-entity coordination.

---

## 1. Entity Relationship Diagram

```
```

**Key Relationships:**
- User → Plan (1:N, cascade delete)
- User → Subject (1:N, cascade delete)
- User → Feedback (1:N, cascade delete)
- Plan → AITask (1:N, cascade delete)
- Subject → AITask (1:N, cascade delete)
- Feedback references generation_id (indirect, not FK)


---

## 2. Calendar Structure: User → Plans → AITasks

The user's calendar is hierarchically structured as:

```
User (john@example.com)
│
├─ Plan (id: 1, date: 2026-01-13, generation_id: gen-abc123)
│  │
│  ├─ AITask (id: 101, ai_task_name: "Calculus Chapter 3", difficulty: 3, priority: 8)
│  │  └─ Subject: Calculus (id: 5)
│  │
│  ├─ AITask (id: 102, ai_task_name: "Physics Lab Report", difficulty: 4, priority: 9)
│  │  └─ Subject: Physics (id: 6)
│  │
│  └─ AITask (id: 103, ai_task_name: "CS Project Review", difficulty: 2, priority: 5)
│     └─ Subject: Computer Science (id: 7)
│
├─ Plan (id: 2, date: 2026-01-14, generation_id: gen-abc123)
│  │
│  ├─ AITask (id: 104, ai_task_name: "Calculus Problem Set", difficulty: 3, priority: 7)
│  │  └─ Subject: Calculus (id: 5)
│  │
│  └─ AITask (id: 105, ai_task_name: "Physics Lecture Notes", difficulty: 2, priority: 6)
│     └─ Subject: Physics (id: 6)
│
├─ Plan (id: 3, date: 2026-01-15, generation_id: gen-abc123)
│  │
│  └─ AITask (id: 106, ai_task_name: "CS Midterm Prep", difficulty: 5, priority: 10)
│     └─ Subject: Computer Science (id: 7)
│
└─ [New generation after feedback]
   
   Plan (id: 4, date: 2026-01-13, generation_id: gen-def456)  ← Regenerated for same date
   │
   ├─ AITask (id: 107, ai_task_name: "Calculus Chapter 3", difficulty: 3, priority: 6)  ← Less priority than before
   │  └─ Subject: Calculus (id: 5)
   │
   └─ AITask (id: 108, ai_task_name: "Physics Prep", difficulty: 2, priority: 4)  ← Reduced scope
      └─ Subject: Physics (id: 6)
```

**Key Structure Principles:**
- **User** has many **Plans** (one per calendar day)
- **Plan** has many **AITasks** (multiple tasks per day)
- **AITask** references exactly one **Subject** (via task_id)
- **Plans** are grouped by `generation_id` (all plans from one generation form a complete schedule)
- When user provides feedback and regenerates, a new `generation_id` is created with fresh Plans and AITasks
- Old generation Plans and AITasks remain in database (for history)

---

## 3. Core Relationships

### User ↔ Plan (One-to-Many)

**Configuration:**
```python
# In User
plans: Mapped[List["Plan"]] = relationship(back_populates="user", cascade="all, delete-orphan")

# In Plan
user: Mapped["User"] = relationship(back_populates="plans")
user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
```

**Cascade Behavior:**
- When a user is deleted, all their plans are automatically deleted
- `delete-orphan` cascade: Plans without a user are deleted
- Used by: User service for user deletion

**Cardinality:** User can have multiple plans; each plan belongs to one user.

---

### Plan ↔ AITask (One-to-Many)

**Configuration:**
```python
# In Plan
ai_tasks: Mapped[List["AITask"]] = relationship(back_populates="plan", cascade="all, delete-orphan")

# In AITask
plan: Mapped["Plan"] = relationship(back_populates="ai_tasks")
plan_id: Mapped[int] = mapped_column(ForeignKey("plans.id", ondelete="CASCADE"))
```

**Cascade Behavior:**
- When a plan is deleted, all its AI tasks are automatically deleted
- This is **critical** because plans are deleted/regenerated during rescheduling
- Prevents orphaned tasks from previous generations

**Cardinality:** Plan can have multiple tasks; each task belongs to one plan.

---

### Subject ↔ AITask (One-to-Many)

**Configuration:**
```python
# In Subject
ai_tasks: Mapped[List["AITask"]] = relationship(back_populates="subject", cascade="all, delete-orphan")

# In AITask
subject: Mapped["Subject"] = relationship(back_populates="ai_tasks")
task_id: Mapped[int] = mapped_column(ForeignKey("subjects.id", ondelete="CASCADE"))
```

**Cascade Behavior:**
- When a subject is deleted, all its AI tasks are deleted
- Prevents tasks from referencing non-existent subjects

**Cardinality:** Subject has many AI tasks; each task references one subject.

**Important:** Note the naming: `task_id` in AITask actually references `Subject.id` (not a separate Task table). The subject IS the task.

---

### User ↔ Subject (One-to-Many)

**Configuration:**
```python
# In User
subjects: Mapped[List["Subject"]] = relationship(back_populates="student")

# In Subject
student: Mapped["User"] = relationship(back_populates="subjects")
student_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
```

**Cascade Behavior:**
- When user is deleted, all their subjects are deleted
- Transitively deletes all AI tasks (via Subject ↔ AITask cascade)

**Cardinality:** User has many subjects; each subject belongs to one user.

---

### User ↔ Feedback (One-to-Many)

**Configuration:**
```python
# In User
feedbacks: Mapped[List["Feedback"]] = relationship(back_populates="user")

# In Feedback
user: Mapped["User"] = relationship(back_populates="feedbacks")
user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
```

**Cascade Behavior:**
- When user is deleted, all their feedback is deleted
- No `delete-orphan` needed; foreign key constraint handles it

**Cardinality:** User has many feedbacks; each feedback belongs to one user.

---

## 4. Non-Traditional Relationships

### Feedback ↔ Generation (Indirect via generation_id)

**This is NOT a direct foreign key relationship.**

**Configuration:**
```python
# In Feedback
generation_id: Mapped[str] = mapped_column(String(36), nullable=False)  # NOT a FK
```

**Why Not a FK?**
- `generation_id` is a UUID that groups plans together
- No dedicated Generation table; it's a virtual concept
- Prevents creation of unnecessary entity

**Usage Pattern:**
```
User generates a plan
  ↓
AiOrchestrator creates a UUID for that generation
  ↓
All plans created in that batch share the same generation_id
  ↓
All feedback for that generation references the same generation_id
  ↓
User provides feedback linked to that generation
  ↓
AiRescheduler uses current + last feedback to regenerate
  ↓
New generation created with new UUID
```

**Unique Constraint:**
```python
UniqueConstraint("user_id", "generation_id", name="uc_user_generation_feedback")
```

Ensures only ONE feedback per generation per user. Prevents conflicts during rescheduling.

---

## 5. Cascade Delete Behavior

When entities are deleted, their child entities are automatically deleted via SQLAlchemy cascades.

**Plan ↔ AITask Cascade:**
When a plan is deleted, all its associated AI tasks are automatically deleted. This is critical during rescheduling, as plans are deleted and regenerated frequently.

**User ↔ Plan/Subject/Feedback Cascade:**
When a user is deleted, all their plans, subjects, and feedback are automatically deleted, maintaining data integrity.

**Subject ↔ AITask Cascade:**
When a subject is deleted, all its associated AI tasks are deleted, preventing orphaned task references.

**Important Note on Feedback:**
When a plan is deleted, its feedback is NOT automatically deleted. Feedback remains linked to the `generation_id` to preserve the rescheduling history.

