# How to simulate and test failure handling in this network in Windows 10:
1. Run the _deploy_renz_windows.sh_ script
2. From the project's root folder run **_python -m src.Router.FailureHandling_test_**
3. When prompted, stop when of the Node docker containers then press Enter to continue
4. Check the logs of the Router docker container, the detected failure and the missing keys caused by the failed node will be displayed there