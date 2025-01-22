import csv
import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import SymmetricAnalysisResult

class Command(BaseCommand):
    help = 'Import symmetric analysis results from CSV file'

    def handle(self, *args, **kwargs):
        csv_file_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', 'results', 'symmetric_analysis_results.csv')
        with open(csv_file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip the header row
            for row in reader:
                SymmetricAnalysisResult.objects.create(
                    user=User.objects.first(),  # Assuming you want to associate with the first user
                    algorithm=row[0],
                    operation=row[1],
                    key_size=int(row[2]),  # Convert key_size to integer
                    file_name=row[3],
                    time_taken=float(row[4])  # Convert time_taken to float
                )
        self.stdout.write(self.style.SUCCESS('Successfully imported CSV data'))