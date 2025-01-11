# HeyGen Assignment

## Overview
This client library allows the user to make calls to the status server. It can create jobs of any time delay, run those jobs, and monitor the status of the running job. It also utilizes several optimizations to lower the number of calls while also not drastically increasing the delay in recieving the updated status of the job.

## Optimizations
### Exponential Backoff
The main optimization is exponential backoff. This optimization start with an small amount of spacing between calls, then exponentially increases the spacing until a certain maximum spacing is reached. 

Through this optimization, the number of calls is greatly reduced, as longer jobs have less calls between them. Furthermore, the presence of a small initial spacing means that shorter jobs do not have to deal with a long delay in receiving updates, as the spacing will still be small during their job.

### Backoff Oscillation
A secondary optimization is backoff oscillation. This is done to reduce delay for longer jobs. Once the maximum spacing is reached for the exponential backoff, the spacing is then lowered by one step before being increased back to the maximum spacing. The spacing then continually oscillates between these two values. 

This optimization helps further reduce the delay in receiving updates, on average. There will be certain cases where this lowered spacing will cut delay by a value up to the backoff factor. A higher backoff factor can lead to a larger drop in delay on average, but could lead to increased delay for shorter jobs. 

### History-Based Calibration
This client library also uses a history-based calibration to automatically adjust the spacing parameters for the exponential backoff. It uses the execution time of the last five jobs to modify the maximum spacing and the initial spacing. If the execution time increases for a job, the spacing parameters are increased, and otherwise, they are decreased.

This optimization helps lower the amount of calls for jobs of different lengths. An increase in execution time means that the jobs are running for longer and increasing the spacing would lower the amount of calls for longer jobs. This optimization utilizes the concept of temporal locality to adapt to repetitions of job lengths from the server.

## Methods
### Initializing the Client
<b>Method:</b> 

`Client(server_url)`: This method initializes the client to hit the status server.

<b>Parameters:</b> 

`server_url`: The url of the status server

<b>Return:</b>

An instance of the client

### Creating a Job
<b>Method:</b> 

`Client.create_job(length=10)`: This method creates a new job and adds it to the job queue in the server

<b>Parameters:</b> 

`length`: The length of the job (in seconds)

<b>Return:</b>

A response from the server indicating the success or failure of the job creation

### Starting a Job
<b>Method:</b> 

`Client.start_job()`: This method starts the next job in the queue


<b>Return:</b>

A response from the server indicating the success or failure of starting the job.

### Monitoring a Job
<b>Method:</b> 

`Client.monitor_job(min_delay=0.5, max_delay=4, backoff_factor=2, oscillation=True, automatic=True)`: This method monitors the status of the current job until the job is completed, and prints out any status changes as they occur

<b>Parameters:</b> 

- `min_delay`: The initial spacing for the exponential backoff
- `max_delay`: The maximum spacing for the exponential backoff
- `backoff_factor`: The growth of the spacing for the exponential backoff
- `oscillation`: Determines if oscillation is being implemented
- `automatic`: Determines if automatic calibration is being implemented
