const { kafka } = require('kafkajs');
const logger = require('../utils/logger');

class KafkaService {
  constructor() {
    this.client = null;
    this.producer = null;
    this.consumer = null;
    this.brokers = process.env.KAFKA_BROKERS ? process.env.KAFKA_BROKERS.split(',') : ['localhost:9092'];
  }

  async init() {
    try {
      this.client = kafka({
        clientId: 'customer-service',
        brokers: this.brokers,
        retry: {
          retries: 5,
          initialRetryTime: 100,
          maxRetryTime: 30000
        }
      });

      this.producer = this.client.producer();
      await this.producer.connect();
      
      logger.info('Kafka producer connected successfully');
    } catch (error) {
      logger.error('Failed to initialize Kafka:', error);
      throw error;
    }
  }

  async publishEvent(topic, message) {
    try {
      await this.producer.send({
        topic,
        messages: [{
          value: JSON.stringify(message),
          timestamp: Date.now().toString()
        }]
      });
      
      logger.info('Event published to Kafka', { topic, messageId: message.id });
    } catch (error) {
      logger.error('Failed to publish event to Kafka:', error);
      throw error;
    }
  }

  async disconnect() {
    try {
      if (this.producer) {
        await this.producer.disconnect();
      }
      if (this.consumer) {
        await this.consumer.disconnect();
      }
      logger.info('Kafka service disconnected');
    } catch (error) {
      logger.error('Error disconnecting Kafka:', error);
    }
  }
}

module.exports = new KafkaService();