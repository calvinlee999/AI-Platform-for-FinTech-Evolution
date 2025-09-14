const express = require('express');
const router = express.Router();
const { KYC, Customer } = require('../models');
const kafkaService = require('../services/kafkaService');
const logger = require('../utils/logger');

// Get KYC status for customer
router.get('/customer/:customerId', async (req, res) => {
  try {
    const kyc = await KYC.findOne({
      where: { customerId: req.params.customerId },
      include: [{ model: Customer, as: 'customer' }]
    });

    if (!kyc) {
      return res.status(404).json({
        error: 'Not Found',
        message: 'KYC record not found for customer',
        correlationId: req.correlationId
      });
    }

    res.json({
      kyc,
      correlationId: req.correlationId
    });
  } catch (error) {
    logger.error('Error fetching KYC:', error);
    res.status(500).json({
      error: 'Internal Server Error',
      message: 'Failed to fetch KYC record',
      correlationId: req.correlationId
    });
  }
});

// Create or update KYC record
router.post('/customer/:customerId', async (req, res) => {
  try {
    const customerId = req.params.customerId;
    const kycData = { ...req.body, customerId };

    // Check if customer exists
    const customer = await Customer.findByPk(customerId);
    if (!customer) {
      return res.status(404).json({
        error: 'Not Found',
        message: 'Customer not found',
        correlationId: req.correlationId
      });
    }

    // Find existing KYC or create new
    let kyc = await KYC.findOne({ where: { customerId } });
    
    if (kyc) {
      await kyc.update(kycData);
    } else {
      kyc = await KYC.create(kycData);
    }

    // Publish KYC event
    await kafkaService.publishEvent('kyc.updated', {
      customerId,
      kycId: kyc.id,
      status: kyc.status,
      level: kyc.level,
      timestamp: new Date().toISOString(),
      correlationId: req.correlationId
    });

    logger.info('KYC record updated', {
      customerId,
      kycId: kyc.id,
      status: kyc.status,
      correlationId: req.correlationId
    });

    res.json({
      kyc,
      correlationId: req.correlationId
    });
  } catch (error) {
    logger.error('Error updating KYC:', error);
    res.status(500).json({
      error: 'Internal Server Error',
      message: 'Failed to update KYC record',
      correlationId: req.correlationId
    });
  }
});

// Update KYC status
router.patch('/:id/status', async (req, res) => {
  try {
    const { status, rejectionReason, approvedBy } = req.body;
    
    const kyc = await KYC.findByPk(req.params.id);
    if (!kyc) {
      return res.status(404).json({
        error: 'Not Found',
        message: 'KYC record not found',
        correlationId: req.correlationId
      });
    }

    const updateData = { status };
    if (status === 'APPROVED') {
      updateData.approvedBy = approvedBy;
      updateData.approvedAt = new Date();
    } else if (status === 'REJECTED') {
      updateData.rejectionReason = rejectionReason;
    }

    await kyc.update(updateData);

    // Publish status change event
    await kafkaService.publishEvent('kyc.status_changed', {
      customerId: kyc.customerId,
      kycId: kyc.id,
      oldStatus: kyc.status,
      newStatus: status,
      approvedBy,
      rejectionReason,
      timestamp: new Date().toISOString(),
      correlationId: req.correlationId
    });

    res.json({
      kyc,
      correlationId: req.correlationId
    });
  } catch (error) {
    logger.error('Error updating KYC status:', error);
    res.status(500).json({
      error: 'Internal Server Error',
      message: 'Failed to update KYC status',
      correlationId: req.correlationId
    });
  }
});

module.exports = router;