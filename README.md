
# Investor Bulletin Project

![Welcome](./imgs/hello-welcome.gif)

> 🚨 This project doesn’t cover all tech/tools in Malaa stack and is only meant to give the initial boost and confidence to start working on Malaa’s codebase
>
## Objectives

You will create a simple API using FastAPI (python web framework), events published & consumed through RabbitMQ, and background tasks managed by Celery to sync stock market data and provide threshold alerting based on user interests.

## Project Context

Stock investments provide one of the highest returns in the market. Even though they are volatile in nature, one can visualize share prices and other statistical factors, which helps keen investors carefully decide on which company they want to spend their earnings on.

This project will allow users to retrieve the latest stock market prices and create alert rules by setting a threshold price for the stock they are interested in and receiving alerts if stocks cross those thresholds.

## High-Level Approach

![high-level](imgs/high-level.png)

## Project phases

- [Phase One - Getting to know FastAPI](./phase_1/README.md)
- [Phase Two - Creating Publisher and Subscriber](./phase_2/README.md)
- [Phase Three - Background tasks](./phase_3/README.md)

## Using Docker Setup

You can make your own setup / but to speed you up, you can use the provided setup. Just ensure you have the docker installed and the docker-compose, then run `make up` to start the containers.

## Deliverables

The solution should be submitted by phase as a GitHub repository with the following:

- Source code with clear comments and documentation.
- Instructions on how to run the code.
- A brief explanation of the solution and any trade-offs made.
## Evaluation

The solution will be evaluated based on the following criteria:

- Correctness and completeness of the solution.
- Code quality and engineering practices.
- Documentation and comments.
- Ease of setup and configuration.
- Solution architecture and design decisions.
- Adherence to the requirements.
