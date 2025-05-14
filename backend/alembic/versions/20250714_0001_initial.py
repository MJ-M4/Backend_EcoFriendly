"""initial

Revision ID: 20250714_0001
Revises: 
Create Date: 2025-07-14 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20250714_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ------------- ROLES -------------
    op.execute(
        """
        CREATE TABLE Roles (
            role_id    TINYINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
            role_name  ENUM('manager','employee') NOT NULL UNIQUE
        ) ENGINE=InnoDB
        """
    )

    # ------------- USERS -------------
    op.execute(
        """
        CREATE TABLE Users (
            user_id        BIGINT UNSIGNED PRIMARY KEY,
            role_id        TINYINT UNSIGNED NOT NULL,
            first_name     VARCHAR(50) NOT NULL,
            last_name      VARCHAR(50) NOT NULL,
            password_hash  VARBINARY(60) NOT NULL,
            is_active      BOOLEAN DEFAULT TRUE,
            created_at     DATETIME DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT fk_users_role
              FOREIGN KEY (role_id) REFERENCES Roles(role_id)
                ON UPDATE CASCADE ON DELETE RESTRICT
        ) ENGINE=InnoDB
        """
    )

    # ------------- BINS -------------
    op.execute(
        """
        CREATE TABLE Bins (
            bin_id       BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
            location     VARCHAR(255) NOT NULL,
            capacity_l   INT UNSIGNED NOT NULL,
            last_emptied DATETIME DEFAULT NULL
        ) ENGINE=InnoDB
        """
    )

    # ------------- BIN READINGS -------------
    op.execute(
        """
        CREATE TABLE BinReadings (
            reading_id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
            bin_id     BIGINT UNSIGNED NOT NULL,
            level_pct  TINYINT UNSIGNED CHECK (level_pct BETWEEN 0 AND 100),
            ts         DATETIME DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT fk_readings_bin
              FOREIGN KEY (bin_id) REFERENCES Bins(bin_id)
                ON DELETE CASCADE
        ) ENGINE=InnoDB
        """
    )

    # ------------- VEHICLES -------------
    op.execute(
        """
        CREATE TABLE Vehicles (
            vehicle_id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
            plate      VARCHAR(20) UNIQUE NOT NULL,
            capacity_l INT UNSIGNED NOT NULL
        ) ENGINE=InnoDB
        """
    )

    # ------------- SHIFTS -------------
    op.execute(
        """
        CREATE TABLE Shifts (
            shift_id     BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
            employee_id  BIGINT UNSIGNED NOT NULL,
            start_ts     DATETIME NOT NULL,
            end_ts       DATETIME NOT NULL,
            approved_by  BIGINT UNSIGNED DEFAULT NULL,
            CONSTRAINT fk_shift_emp
              FOREIGN KEY (employee_id) REFERENCES Users(user_id)
                ON DELETE CASCADE,
            CONSTRAINT fk_shift_mngr
              FOREIGN KEY (approved_by) REFERENCES Users(user_id)
                ON DELETE SET NULL
        ) ENGINE=InnoDB
        """
    )

    # ------------- PAYROLL -------------
    op.execute(
        """
        CREATE TABLE Payroll (
            payroll_id   BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
            employee_id  BIGINT UNSIGNED NOT NULL,
            month        INT UNSIGNED NOT NULL,
            amount_nis   DECIMAL(10,2) NOT NULL,
            paid         BOOLEAN DEFAULT FALSE,
            CONSTRAINT fk_pay_emp
              FOREIGN KEY (employee_id) REFERENCES Users(user_id)
                ON DELETE CASCADE
        ) ENGINE=InnoDB
        """
    )


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS Payroll")
    op.execute("DROP TABLE IF EXISTS Shifts")
    op.execute("DROP TABLE IF EXISTS Vehicles")
    op.execute("DROP TABLE IF EXISTS BinReadings")
    op.execute("DROP TABLE IF EXISTS Bins")
    op.execute("DROP TABLE IF EXISTS Users")
    op.execute("DROP TABLE IF EXISTS Roles")