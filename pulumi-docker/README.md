
# Docker multi-container deployment


## Prerequisites

To run this example:

  - make sure [Docker](https://docs.docker.com/engine/installation/) is installed and running
  - make sure [Pulumi](https://www.pulumi.com/docs/get-started/install/) is installed

  - setup pulumi state to local file for testing this ( for testing use blank passphrase, just hit enter when asked)

    ```

      $ pulumi login file://~


    ```


## Running the App

1.  Create a new stack:

    ```
    $ pulumi stack init dev
    ```

1.  Start your virtual environment:

    ```
    $ python -m venv venv && source venv/bin/activate
    ```

1. Restore your pypi packages:

    ```
    $ pip3 install -r requirements.txt
    ```

2.  Preview and deploy the app via `pulumi up`. The preview will take a few minutes, as it builds a Docker container. A total of 19 resources are created.

    ```
    $ pulumi up
    ```

 
    Wait and check if all the containers are up


    ```

    $ docker ps -a


    ```   

3.  View the endpoint URL, and run curl:

    ```bash
    $ pulumi stack output
    Current stack outputs (1)
        OUTPUT                  VALUE
        url                http://localhost


    ```


To clean up resources, run `pulumi destroy` and answer the confirmation question at the prompt.
