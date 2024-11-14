from src.connector import apifetch
from src.util import config
from src.rest import apiconnector
from PyQt5.QtCore import QThread, pyqtSignal
from src.GUI.FetchLineWorker import FetchLineWorker
import traceback


class FetchDataWorker(QThread):
    #define custom signals
    dataFetched = pyqtSignal(list)
    fetchFailed = pyqtSignal(str)
    fetchStarted = pyqtSignal()
    
    def __init__(self, vcf_data):
        super().__init__()
        api_config = config.load_config("config/API.ini", "api")
        self.api_address = api_config['host']
        self.api_port = api_config['port']
        self.vcf_data = vcf_data
        self.openJobs = list(range(0, len(vcf_data)))
        self.runningJobs = list(range(0, len(vcf_data)))
        
    running_threads = 0
    thread_max = 20000
    fetched_data = []
    workers = []
        
    def run(self):
        """the execution logic for the API request

        Args:
            vcf_data (_type_): a list of vcf entries to be annotated
        """
        try:
            #emit a signal indicating the fetch has started
            self.fetchStarted.emit()
            
            if(len(self.openJobs) == 0):
                raise Exception('No data!')
            
            startNext = True
            while startNext:
                startNext = self.startNextThread()
            
        except Exception as e:
            print("Exception: " + str(e))
            traceback.print_exc()
            self.fetchFailed.emit(f"Failed to fetch data: {str(e)}")

    def onDataFetched(self, jobNumber: int, data: dict):
        self.running_threads = self.running_threads-1
        self.runningJobs.remove(jobNumber)
        self.fetched_data.append(data)
        self.startNextThread()

    def onFetchStarted(self):
        pass

    def onFetchFailed(self, jobNumber, msg):
        self.running_threads = self.running_threads-1
        self.runningJobs.remove(jobNumber)
        self.startNextThread()

    def startNextThread(self):
        if(self.running_threads < self.thread_max) and len(self.openJobs) > 0:
            nextJobNum = self.openJobs[0]
            self.openJobs.remove(nextJobNum)
            self.running_threads = self.running_threads + 1
            worker = FetchLineWorker(nextJobNum, self.vcf_data[nextJobNum])
            worker.dataFetched.connect(self.onDataFetched)
            worker.fetchStarted.connect(self.onFetchStarted)
            worker.fetchFailed.connect(self.onFetchFailed)
            worker.start()
            self.workers.append(worker)
        elif len(self.openJobs) > 0:
            return False
        else:
            self.dataFetched.emit(self.merge_vcf_annotations(self.vcf_data, self.fetched_data))       

    def merge_vcf_annotations(self, vcf_data, annotated_data):
        merged_data = vcf_data.copy()
        for entry1 in vcf_data:
            for entry2 in annotated_data:
                if str(entry1['CHROM']) == str(entry2['chrom']) and \
                int(entry1['POS']) == int(entry2['pos']) and \
                entry1['REF'] == entry2['ref'] and \
                entry1['ALT'] == entry2['alt']:
                    # found annotation for entry1
                    merged_data.append(entry1 | entry2)
                    merged_data.remove(entry1)

        return merged_data