import mysql.connector
from mysql.connector import errorcode
from typing import Optional, List, Dict
import datetime


class DatabaseManager:
    __instance = None

    def __init__(self):
        self.connection = None
        self.config = {
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'database': 'smartFace'
        }

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = DatabaseManager()
            cls.__instance.initialize_database()
        return cls.__instance

    def connect(self) -> Optional[mysql.connector.MySQLConnection]:
        try:
            self.connection = mysql.connector.connect(**self.config)
            return self.connection
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                return self._create_database()
            print(f"Database connection error: {err}")
            return None

    def _create_database(self) -> Optional[mysql.connector.MySQLConnection]:
        try:
            temp_conn = mysql.connector.connect(
                host=self.config['host'],
                user=self.config['user'],
                password=self.config['password']
            )
            cursor = temp_conn.cursor()
            cursor.execute(f"CREATE DATABASE {self.config['database']} DEFAULT CHARACTER SET 'utf8mb4'")
            cursor.close()
            temp_conn.close()
            return mysql.connector.connect(**self.config)
        except mysql.connector.Error as err:
            print(f"Database creation error: {err}")
            return None

    def initialize_database(self):
        TABLES = {
            'admin': (
                "CREATE TABLE IF NOT EXISTS `admin` ("
                "  `admin_id` INT AUTO_INCREMENT PRIMARY KEY,"
                "  `username` VARCHAR(50) NOT NULL UNIQUE,"
                "  `password` VARCHAR(255) NOT NULL,"
                "  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
                ") ENGINE=InnoDB"
            ),
            'departments': (
                "CREATE TABLE IF NOT EXISTS `departments` ("
                "  `department_id` INT AUTO_INCREMENT PRIMARY KEY,"
                "  `name` VARCHAR(50) NOT NULL UNIQUE,"
                "  `description` TEXT,"
                "  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
                ") ENGINE=InnoDB"
            ),
            'employees': (
                "CREATE TABLE IF NOT EXISTS `employees` ("
                "  `employee_id` INT AUTO_INCREMENT PRIMARY KEY,"
                "  `nom` VARCHAR(50) NOT NULL,"
                "  `prenom` VARCHAR(50) NOT NULL,"
                "  `email` VARCHAR(100) UNIQUE,"
                "  `poste` VARCHAR(50),"
                "  `department_id` INT,"
                "  `image` LONGBLOB,"
                "  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
                "  FOREIGN KEY (`department_id`) REFERENCES `departments` (`department_id`)"
                ") ENGINE=InnoDB"
            ),
            'project': (
                "CREATE TABLE IF NOT EXISTS `project` ("
                "  `project_id` INT AUTO_INCREMENT PRIMARY KEY,"
                "  `nom` VARCHAR(100) NOT NULL,"
                "  `description` TEXT,"
                "  `date_debut` DATE,"
                "  `date_fin` DATE,"
                "  `statut` ENUM('En cours','Terminé','En attente') DEFAULT 'En attente',"
                "  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
                ") ENGINE=InnoDB"
            ),
            'attendance': (
                "CREATE TABLE IF NOT EXISTS `attendance` ("
                "  `attendance_id` INT AUTO_INCREMENT PRIMARY KEY,"
                "  `employee_id` INT NOT NULL,"
                "  `date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
                "  `status` ENUM('in','out') NOT NULL,"
                "  FOREIGN KEY (`employee_id`) REFERENCES `employees` (`employee_id`)"
                ") ENGINE=InnoDB"
            ),
            'affectation': (
                "CREATE TABLE IF NOT EXISTS `affectation` ("
                "  `affectation_id` INT AUTO_INCREMENT PRIMARY KEY,"
                "  `employee_id` INT NOT NULL,"
                "  `project_id` INT NOT NULL,"
                "  `role` VARCHAR(50),"
                "  `date_affectation` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
                "  FOREIGN KEY (`employee_id`) REFERENCES `employees` (`employee_id`),"
                "  FOREIGN KEY (`project_id`) REFERENCES `project` (`project_id`),"
                "  UNIQUE KEY `unique_affectation` (`employee_id`, `project_id`)"
                ") ENGINE=InnoDB"
            ),
            'presence': (
                "CREATE TABLE IF NOT EXISTS `presence` ("
                "  `presence_id` INT AUTO_INCREMENT PRIMARY KEY,"
                "  `employee_id` INT NOT NULL,"
                "  `date` DATE NOT NULL,"
                "  `heure_arrivee` TIME,"
                "  `heure_depart` TIME,"
                "  FOREIGN KEY (`employee_id`) REFERENCES `employees` (`employee_id`)"
                ") ENGINE=InnoDB"
            )
        }

        if not self.connect():
            return False

        cursor = self.connection.cursor()
        for name, ddl in TABLES.items():
            try:
                cursor.execute(ddl)
            except mysql.connector.Error as err:
                print(f"Error creating table {name}: {err}")
        cursor.close()
        return True

    def execute_query(self, query: str, params=None, fetch=None):
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            result = None
            if fetch == 'one':
                result = cursor.fetchone()
            elif fetch == 'all':
                result = cursor.fetchall()
            else:
                self.connection.commit()
            cursor.close()
            return result
        except mysql.connector.Error as err:
            print(f"Query execution error: {err}")
            return None


# Interface Functions

def check_login(username: str, password: str) -> bool:
    db = DatabaseManager.get_instance()
    query = "SELECT * FROM admin WHERE username = %s AND password = %s"
    return db.execute_query(query, (username, password), 'one') is not None


def insert_employee(nom: str, prenom: str, email: str, poste: str, department_id: int, image_data: bytes):
    db = DatabaseManager.get_instance()
    query = """INSERT INTO employees (nom, prenom, email, poste, department_id, image)
               VALUES (%s, %s, %s, %s, %s, %s)"""
    db.execute_query(query, (nom, prenom, email, poste, department_id, image_data))


def get_employee_list() -> List[Dict]:
    db = DatabaseManager.get_instance()
    query = """SELECT e.*, d.name as department_name
               FROM employees e
               LEFT JOIN departments d ON e.department_id = d.department_id"""
    return db.execute_query(query, fetch='all') or []


def get_departments() -> List[tuple]:
    db = DatabaseManager.get_instance()
    query = "SELECT department_id, name FROM departments"
    result = db.execute_query(query, fetch='all')
    return [(row['department_id'], row['name']) for row in result] if result else []


def search_employee(search_term: str) -> List[Dict]:
    db = DatabaseManager.get_instance()
    query = """SELECT e.*, d.name as department_name
               FROM employees e
               LEFT JOIN departments d ON e.department_id = d.department_id
               WHERE e.nom LIKE %s OR e.prenom LIKE %s OR d.name LIKE %s"""
    pattern = f"%{search_term}%"
    return db.execute_query(query, (pattern, pattern, pattern), 'all') or []


def get_worked_hours_today(employee_id: int) -> str:
    today = datetime.date.today().isoformat()
    return calculate_work_hours(employee_id, today)


def get_worked_hours_month(employee_id: int) -> str:
    db = DatabaseManager.get_instance()
    query = """SELECT date, status
               FROM attendance
               WHERE employee_id = %s AND MONTH(date) = MONTH(CURDATE())
               ORDER BY date"""
    records = db.execute_query(query, (employee_id,), 'all') or []
    return _compute_total_worked_time(records)


def calculate_work_hours(employee_id: int, date: str) -> str:
    db = DatabaseManager.get_instance()
    query = """SELECT date, status
               FROM attendance
               WHERE employee_id = %s AND DATE(date) = %s
               ORDER BY date"""
    records = db.execute_query(query, (employee_id, date), 'all') or []
    return _compute_total_worked_time(records)


def _compute_total_worked_time(records):
    total_seconds = 0
    check_in = None
    for record in records:
        if record['status'] == 'in':
            check_in = record['date']
        elif record['status'] == 'out' and check_in:
            total_seconds += (record['date'] - check_in).total_seconds()
            check_in = None
    if check_in:
        total_seconds += (datetime.datetime.now() - check_in).total_seconds()
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    return f"{hours:02d}:{minutes:02d}"


def get_dep():
    return None