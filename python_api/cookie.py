import time
import json


class Cookie:

    FOREVER = -999

    def __init__(self):
        self.begin_time = 0
        self.expired_time = 0
        self.end_time = 0

        self.value = None
        self.default_value = None

    def has_loaded(self):
        return self.end_time == self.FOREVER \
            or time.time() <= self.end_time

    def load(self):
        '''
        Notice: must return boolean
        '''
        raise NotImplementedError('Method not implemented!')

    def check_and_loaded(self):
        if self.has_loaded():
            return True

        return self.load()

    def set_forever(self):
        self.end_time = self.FOREVER

    def set_end_time(self, end_time):
        self.end_time = end_time

    def set_expired_time(self, expired_time, *, begin_time=None):
        if begin_time is None:
            self.begin_time = time.time()
        else:
            self.begin_time = begin_time

        self.expired_time = expired_time
        self.end_time = self.begin_time + expired_time

    def get_value(self):
        if not self.check_and_loaded():
            self.value = self.default_value

        return self.value

    # 文件接口
    # ------------
    def read(self, f, keys):
        try:
            # self.json_dict = json.load(f)
            self.json_dict = json.loads(f.read().decode('utf8'))
        except json.JSONDecodeError:
            self.json_dict = {}

        now_value = self.json_dict
        for key in keys:
            try:
                now_value = now_value[str(key)]
            except KeyError:
                return None

        return now_value

    def write(self, f, keys, value):
        now_value = self.json_dict
        for key in keys[:-1]:
            key_str = str(key)
            if key_str not in now_value:
                now_value[key_str] = {}

            now_value = now_value[key_str]

        now_value[keys[-1]] = value
        # 清空原文件
        f.seek(0)
        f.truncate()
        # json.dump(self.json_dict, f)
        f.write(json.dumps(self.json_dict).encode('utf8'))

    def read_pb(self, f, pb):
        pb.ParseFromString(f.read())

    def write_pb(self, f, pb):
        f.seek(0)
        f.truncate()
        f.write(pb.SerializeToString())
