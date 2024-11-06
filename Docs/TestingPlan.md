# Testing Plan for Online Chinese Food Shop

---

## System Analysis and Identification of Potential Failure Points Under High Load

### Potential Failure Points Under High Load:

1. **Database**:
    - **Failure Point**: With a high number of simultaneous requests to the database (e.g., when many users are buying food simultaneously), there can be **bottlenecks** in transaction execution.
    - **Conditions for Failure**:
        - Transaction locking due to large amounts of data or concurrent access to the same records/tables.
        - Exhaustion of the connection pool to the database.
        - Timeout issues caused by database overload.
    - **Consequences**: The system cannot complete transactions, delays in saving data, or failure to commit transactions.

2. **Transaction System (ordering food)**:
    - **Failure Point**: High volumes of simultaneous financial operations can lead to transaction collisions or difficulties in processing large data streams.
    - **Conditions for Failure**:
        - Incorrect transaction completion or "hanging" transactions due to large queues.
        - Transaction failure due to the database being unable to process many simultaneous operations.
        - System overload due to incorrect configuration of connection pools or resource limits.
    - **Consequences**: Incorrect user balance updates, failure during buy/sell operations.

3. **Connection Pool and HTTP Requests**:
    - **Failure Point**: A large number of simultaneous requests (e.g., buying or selling metals) can exhaust the connection pool to the database or external services.
    - **Conditions for Failure**:
        - Exceeding the number of simultaneous connections to the database or external API.
        - Exhaustion of server resources (including CPU and memory).
    - **Consequences**: Inability to handle new requests, system slowdown, or complete system failure.

4. **Network Infrastructure**:
    - **Failure Point**: Server or network infrastructure overload due to many requests to the server.
    - **Conditions for Failure**:
        - Exceeding network bandwidth.
        - Server crashes due to insufficient resources.
    - **Consequences**: System access issues, failure to serve users.

---

## Plan for System Testing Under Load

### 1. **Load Testing**:
- **Objective**: To check how the system behaves under increasing numbers of concurrent users and requests.
- **Test**:
    - Use tools like **Apache JMeter**, **Gatling**, or **Locust** to simulate a large number of simultaneous requests to the API.
    - Create test scenarios for ordering food requests.
    - Simulate multiple users logging in and performing transactions concurrently.
- **Expected Results**: The system should support a certain number of simultaneous users without significant performance degradation or failure.

### 2. **Stress Testing**:
- **Objective**: To check how the system withstands extreme conditions (load beyond expected limits).
- **Test**:
    - Gradually increase the number of requests to the system and observe when it starts failing.
    - Simulate high loads on the database and external APIs.
- **Expected Results**: Determine the point at which the system begins to fail (e.g., increased latency or complete crash).

### 3. **Connection Pool Testing**:
- **Objective**: To check how the system manages connection pools for database or external service requests.
- **Test**:
    - Create a load that causes many concurrent requests requiring access to the database or external APIs.
    - Measure how the system handles the connection pool and whether there are any blocking issues.
- **Expected Results**: The system should efficiently manage the connection pool without causing request failures.

---

## Test Protocols Documentation

### Example of a Test Protocol:

| **Test**                        | **Description**                                    | **Expected Result**                                            | **Outcome**       |
|---------------------------------|----------------------------------------------------|----------------------------------------------------------------|-------------------|
| Load Test for Transactions      | Simultaneously execute 100 orders transactions | System processes all requests without failure, minimal delays  | Success / Failure |
| Stress Test for Database        | Increase the number of concurrent requests to 5000 | Request processing time does not exceed the expected threshold | Success / Failure |
| External API Failure Simulation | Simulate delays or unavailability of external API  | System should handle API failures and not freeze or crash      | Success / Failure |

### Explanation of Decisions:
- If the system cannot process requests within the defined time limit (e.g., exceeding 10 seconds), the database handling or connection pooling should be optimized.
- In case of external API failures, the system should either fall back to cached data or inform the user about temporary price unavailability.

---

## Conclusion

By following this plan, you will be able to assess the system's stability under high load conditions and ensure it can handle stress effectively. The testing should help identify potential bottlenecks and improve the system's reliability when serving many users concurrently.

---