-- Supports the frontend's actual signup/profile flow: signup only
-- collects name/email/password; everything else (DOB, nationality,
-- state, academic details) is filled in later via PUT /student/profile.
-- gender is never collected by the current profile form at all — kept
-- nullable so gender-based eligibility rules simply won't fire for
-- these profiles until/unless the frontend adds that field.

ALTER TABLE student
    ALTER COLUMN date_of_birth DROP NOT NULL,
    ALTER COLUMN nationality DROP NOT NULL,
    ALTER COLUMN state DROP NOT NULL,
    ALTER COLUMN gender DROP NOT NULL;

-- institution: the frontend collects this per qualification (including
--   the student's current college) but no column existed for it.
-- year_of_study_label: the frontend's "yearOfStudy" is a string like
--   'Final Year'/'Graduated', not the existing numeric current_year —
--   kept as a separate column rather than overloading current_year.
ALTER TABLE education
    ADD COLUMN IF NOT EXISTS institution VARCHAR(255),
    ADD COLUMN IF NOT EXISTS year_of_study_label VARCHAR(50),
    -- Distinguishes the single "previousQualification" entry (shown
    -- only when hasHigherQualification is checked) from the regular
    -- repeatable "qualifications" list — both use the same shape on
    -- the frontend, so this flag is what tells them apart on read-back.
    ADD COLUMN IF NOT EXISTS is_higher_qualification BOOLEAN;

-- New table: the frontend's profile form collects repeatable work
-- experience entries with no existing home in the schema.
CREATE TABLE IF NOT EXISTS work_experience (
    work_experience_id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES student(student_id),
    company VARCHAR(255),
    role VARCHAR(255),
    duration VARCHAR(100)
);