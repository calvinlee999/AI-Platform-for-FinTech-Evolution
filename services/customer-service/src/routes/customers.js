const express = require('express');
const router = express.Router();
const { Customer, KYC, Address, Document } = require('../models');
const kafkaService = require('../services/kafkaService');
const logger = require('../utils/logger');

// Get all customers with pagination
router.get('/', async (req, res) => {
  try {
    const page = parseInt(req.query.page) || 1;
    const limit = parseInt(req.query.limit) || 10;
    const offset = (page - 1) * limit;

    const customers = await Customer.findAndCountAll({
      limit,
      offset,
      include: [
        { model: KYC, as: 'kyc' },
        { model: Address, as: 'addresses' }
      ],
      order: [['createdAt', 'DESC']]
    });

    res.json({
      customers: customers.rows,
      pagination: {
        page,
        limit,
        total: customers.count,
        pages: Math.ceil(customers.count / limit)
      },
      correlationId: req.correlationId
    });
  } catch (error) {
    logger.error('Error fetching customers:', error);
    res.status(500).json({
      error: 'Internal Server Error',
      message: 'Failed to fetch customers',
      correlationId: req.correlationId
    });
  }
});

// Get customer by ID
router.get('/:id', async (req, res) => {
  try {
    const customer = await Customer.findByPk(req.params.id, {
      include: [
        { model: KYC, as: 'kyc' },
        { model: Address, as: 'addresses' },
        { model: Document, as: 'documents' }
      ]
    });

    if (!customer) {
      return res.status(404).json({
        error: 'Not Found',
        message: 'Customer not found',
        correlationId: req.correlationId
      });
    }

    res.json({
      customer,
      correlationId: req.correlationId
    });
  } catch (error) {
    logger.error('Error fetching customer:', error);
    res.status(500).json({
      error: 'Internal Server Error',
      message: 'Failed to fetch customer',
      correlationId: req.correlationId
    });
  }
});

// Create new customer
router.post('/', async (req, res) => {
  try {
    const customerData = req.body;
    
    // Generate customer number
    const timestamp = Date.now().toString();
    const random = Math.random().toString(36).substr(2, 6).toUpperCase();
    customerData.customerNumber = `CUST-${timestamp}-${random}`;

    const customer = await Customer.create(customerData);

    // Publish customer created event
    await kafkaService.publishEvent('customer.created', {
      id: customer.id,
      customerNumber: customer.customerNumber,
      email: customer.email,
      timestamp: new Date().toISOString(),
      correlationId: req.correlationId
    });

    logger.info('Customer created successfully', {
      customerId: customer.id,
      customerNumber: customer.customerNumber,
      correlationId: req.correlationId
    });

    res.status(201).json({
      customer,
      correlationId: req.correlationId
    });
  } catch (error) {
    logger.error('Error creating customer:', error);
    res.status(500).json({
      error: 'Internal Server Error',
      message: 'Failed to create customer',
      correlationId: req.correlationId
    });
  }
});

// Update customer
router.put('/:id', async (req, res) => {
  try {
    const customer = await Customer.findByPk(req.params.id);
    
    if (!customer) {
      return res.status(404).json({
        error: 'Not Found',
        message: 'Customer not found',
        correlationId: req.correlationId
      });
    }

    await customer.update(req.body);

    // Publish customer updated event
    await kafkaService.publishEvent('customer.updated', {
      id: customer.id,
      customerNumber: customer.customerNumber,
      changes: req.body,
      timestamp: new Date().toISOString(),
      correlationId: req.correlationId
    });

    res.json({
      customer,
      correlationId: req.correlationId
    });
  } catch (error) {
    logger.error('Error updating customer:', error);
    res.status(500).json({
      error: 'Internal Server Error',
      message: 'Failed to update customer',
      correlationId: req.correlationId
    });
  }
});

module.exports = router;