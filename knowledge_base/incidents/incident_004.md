# Incident 004: Checkout Latency From Connection Pool Exhaustion

Date: 2026-04-21  
Service: order-service  
Severity: high

## Summary
Checkout p95 rose above 2.8s and order submissions timed out. Payment gateway health was normal. Logs showed database connection acquisition timeouts from order-service workers.

## Signals
- `db.pool.in_use` stayed above 95%.
- `order.checkout.p95` rose steadily for 18 minutes.
- No provider 5xx increase.

## Cause
A release increased worker concurrency without increasing transaction discipline. Connections were held during payment-service calls.

## Resolution
Rolled back order-service and restarted saturated workers. Latency returned to normal within 8 minutes.

## Retrieval Notes
Similar to slow database incidents, but the key clue was pool acquisition timeout rather than query duration.
