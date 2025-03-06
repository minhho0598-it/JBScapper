import sqlite3
import json
import configparser
from pathlib import Path

class DatabaseManager:
    def __init__(self, config_file='config/appsettings.ini'):
        config = configparser.ConfigParser()
        config_file_path = Path(__file__).parent.parent / config_file
        config.read(config_file_path)

        self.db_type = config['DATABASE']['DB_TYPE']
        self.db_path = config['DATABASE']['DB_PATH']
        # self.db_host = config['DATABASE']['DB_HOST'] #you can uncomment this lines when change to other database
        # self.db_port = config['DATABASE']['DB_PORT']
        # self.db_user = config['DATABASE']['DB_USER']
        # self.db_password = config['DATABASE']['DB_PASSWORD']
        # self.db_name = config['DATABASE']['DB_NAME']
        self.create_table()

    def create_table(self):
        """Creates the upwork_jobs table if it doesn't exist."""
        if self.db_type == 'sqlite':
            conn = None
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS upwork_jobs (
                        job_id TEXT PRIMARY KEY,
                        title TEXT,
                        description TEXT,
                        category TEXT,
                        budget REAL,
                        date_posted INTEGER,
                        client_location TEXT,
                        skills TEXT
                    )
                """)
                conn.commit()
            except sqlite3.Error as e:
                raise RuntimeError(f"Error creating table: {e}")
            finally:
                if conn:
                    conn.close()
        # you can add another code for another database here
        else:
            raise RuntimeError(f'This application only support sqlite at the moment')

    def save_job_to_db(self, job):
        """Saves a single Upwork job to the database."""
        if self.db_type == 'sqlite':
            conn = None
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR IGNORE INTO upwork_jobs (job_id, title, description, category, budget, date_posted, client_location, skills)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    job.get('id'),
                    job.get('title'),
                    job.get('description'),
                    job.get('category'),
                    job.get('budget'),
                    job.get('date_posted'),
                    job.get('client_location'),
                    json.dumps(job.get('skills'))
                ))
                conn.commit()
            except sqlite3.Error as e:
                raise RuntimeError(f"Error saving job to database: {e}")
            finally:
                if conn:
                    conn.close()
        else:
            raise RuntimeError(f'This application only support sqlite at the moment')

    def save_jobs_to_db(self, jobs):
        for job in jobs:
            # Modify to save only job_node
            if 'node' in job:
                job_node = job['node']
                if job_node:
                    self.save_job_to_db({
                        'id': job_node.get('id'),
                        'title': job_node.get('title'),
                        'description': job_node.get('description'),
                        'category': job_node.get('category'),
                        'budget': job_node.get('budget'),
                        'date_posted': job_node.get('datePosted'),
                        'client_location': job_node.get('client', {}).get('location', {}).get('country'),
                        'skills': job_node.get('skills')
                    })
