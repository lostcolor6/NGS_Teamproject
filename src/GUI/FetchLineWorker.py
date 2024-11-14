from src.util import config
from PyQt5.QtCore import QThread, pyqtSignal
from src.rest.fetch import fetch_url_text
from src.GUI.VEPParser import get_vep_columns
import traceback


class FetchLineWorker(QThread):
    fetchStarted = pyqtSignal()
    dataFetched = pyqtSignal(int, dict)
    fetchFailed = pyqtSignal(int, str)
    
    api_url = "http://127.0.0.1:8000/vep"
    
    def __init__(self, jobNum, entry):
        super().__init__()
        api_config = config.load_config("config/API.ini", "api")
        self.api_address = api_config['host']
        self.api_port = api_config['port']
        self.entry = entry
        self.jobNum = jobNum
        
    def run(self):
        """the execution logic for the API request

        Args:
            vcf_data (_type_): a list of vcf entries to be annotated
        """
        self.fetchStarted.emit()
        entry = self.entry
        
        try:
            api_req = {"chrom": str(entry["CHROM"]), 
                       "pos": int(entry["POS"]), 
                       "ref": str(entry["REF"]), 
                       "alt": str(entry["ALT"])}
            db_response = fetch_url_text(self.api_url, api_req)
            if db_response == []:
                raise Exception("No data fetched from the API")
            elif len(db_response) > 1:
                raise Exception("Multiple entries for one vcf.")
            else:
                parsed_response = get_vep_columns(db_response[0])
                self.dataFetched.emit(self.jobNum, parsed_response)
                
        except Exception as e:
            print("Exception: " + str(e))
            traceback.print_exc()
            self.fetchFailed.emit(self.jobNum, f"Failed to fetch data: {str(e)}")