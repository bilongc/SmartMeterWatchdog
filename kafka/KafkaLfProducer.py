import sys
from kafka.client import KafkaClient
from kafka.producer import KeyedProducer
from ConfigParser import SafeConfigParser
from MeterReader import MeterLfReader

class KafkaLfProducer(object):
    def __init__(self, addr, conf_file):
        self.parser = SafeConfigParser()
        self.parser.read(conf_file)
        install_dir = self.parser.get('smw_tool', 'INSTALL_DIR')
        zipdb_file = self.parser.get('smw_tool', 'ZIP_DB_FILE') 

        self.client = KafkaClient(addr)
        self.producer = KeyedProducer(self.client)
        self.meterReader = MeterLfReader(10,
                                         install_dir + "/data/low_freq/", 
                                         install_dir + "/" + zipdb_file)

    def produce_msgs(self, source_symbol):
        msg_cnt = 0

        while True:
            msg = self.meterReader.getRecord()

            print msg

#            self.producer.send_messages('price_data_part6', source_symbol, msg)
            msg_cnt += 1

if __name__ == "__main__":
    args = sys.argv
    conf_file = str(args[1])
    ip_addr = str(args[2])
    partition_key = str(args[3])
    prod = KafkaLfProducer(ip_addr, conf_file)
    prod.produce_msgs(partition_key) 