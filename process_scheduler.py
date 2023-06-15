import multiprocessing


class ProcessScheduler(object):

    results = multiprocessing.Manager().dict()

    def __init__(self, core=None, job_list=None):
        self.running = True
        self.core = core
        self._all_process = []
        self.total_process_count = 0
        self.max_count = 3
        self.job_list = job_list
        self.activity_process_count = 0

    def initialize(self):
        pass

    def get_job(self):
        job_name = None
        if len(self.job_list) > 0:
            job_name = self.job_list.pop(0)
            return job_name

    def update(self, process=None):
        if process is not None:
            self._all_process.append(process)
            self.activity_process_count += 1
            return

        for process in self._all_process:
            if process.is_alive() is False:
                self._all_process.remove(process)
                self.activity_process_count -= 1

    def start(self):
        self.initialize()
        while self.running:
            self.update()
            if len(self.job_list) == 0 and self.activity_process_count == 0:
                self.stop()
                break
            if self.max_count and self.activity_process_count >= self.max_count:
                continue
            job_name = self.get_job()
            if job_name:
                self.total_process_count += 1
                # process = multiprocessing.Process(target=self.core, args=(job_name,))
                process = multiprocessing.Process(target=self.core, kwargs=job_name)
                process.daemon = True
                process.start()
                self.update(process)

    def stop(self):
        self.running = False
