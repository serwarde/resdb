# How to simulate and test failure handling in this network in Windows 10:
1. Run the _deploy_renz_windows.sh_ script
2. From the project's root folder run **_python -m src.NamingService.NamingService_test_**
3. From the project's root folder run **_python -m src.Router.rendezvousHashing_test_**
4. From the project's root folder run **_python -m src.Router.FailureHandling_test_**
5. When prompted, press Enter to continue
6. Re-run the **_python -m src.Router.FailureHandling_test_**
7. This time before pressing Enter, make sure to stop one of the docker containers (preferably one with a lot of key-value-pairs)
8. Press Enter
9. Check the logs of the Router docker container, the detected failure and the missing keys caused by the failed node will be displayed there