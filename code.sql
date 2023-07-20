CREATE TABLE `positions` (
  `id_position` integer PRIMARY KEY,
  `name_position` text
);

CREATE TABLE `users` (
  `id_user` integer PRIMARY KEY,
  `id_position_user` integer, --REF
  `name` text,
  FOREIGN KEY (id_position_user) REFERENCES positions(id_position) ON DELETE CASCADE
);

CREATE TABLE `type_event` (
  `id_type` integer PRIMARY KEY,
  `name_type` text
);

CREATE TABLE `event` (
  `id_event` integer PRIMARY KEY,
  `name_object` text,
  `id_object_type` integer, --REF
  `group` text,
  FOREIGN KEY (id_object_type) REFERENCES type_event(id_type) ON DELETE CASCADE
);

CREATE TABLE `schedule_list` (
  `id_schedule` integer PRIMARY KEY,
  `id_employee_schedule` integer, --REF
  `id_event_schedule` integer, --REF
  `id_employer_schedule` integer, --REF
  FOREIGN KEY (id_employee_schedule) REFERENCES users(id_user) ON DELETE CASCADE ,
  FOREIGN KEY (id_event_schedule) REFERENCES event(id_event) ON DELETE CASCADE ,
  FOREIGN KEY (id_employer_schedule) REFERENCES users(id_user) ON DELETE CASCADE
);

CREATE TABLE `daily_task` (
    `id_task` integer PRIMARY KEY,
    `task_date` date,
    'id_schedule_task' integer, --REF
    `mark` integer default false,
    `description` text,
    FOREIGN KEY (id_schedule_task) REFERENCES schedule_list(id_schedule) ON DELETE CASCADE
)