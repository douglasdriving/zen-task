CREATE TABLE task_dependencies (
    task_id INTEGER NOT NULL,
    dependency_task_id INTEGER NOT NULL,
    PRIMARY KEY (task_id, dependency_task_id),
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE,
    FOREIGN KEY (dependency_task_id) REFERENCES tasks(id) ON DELETE CASCADE
);