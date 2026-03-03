Notes:


In the example for maven:
    - might need to specify how to find the version and how to set up the pom.xml file (this seems to be missing in some tests)


Not sure what should be first to check for the agent. I think this changes depending on the prompt, might need to specify always. 
Option 1:
    DevOps platform examples 
    Scanner and how to use it

Option 2:
    Scanner and how to use it
    DevOps platform 




A couple of notes
For step 1, not sure if adding the directory might later impact how other users have their agent/skills set up. So not sure this would be the correct change. I like the change in the prompt of READ <skill> using read tool since it is more exact.
What would be the workflow diagram you are proposing?



02/16
For the maven scanner, might need to specify that the version of the plugin needs to be added to either the pom.xml file or in the maven command in the pipeline. Had a couple of examples where it is retrieving the version but not adding the version of the plugin anywhere.

Could it be that the copilot cli has issues with some tools? could it be that vs code has more tools for the LLM to use?




i have identified a proper set of webpages that will have the version of the plugin/scanner versions.
Gradle:
https://downloads.sonarsource.com/sonarqube/update/scannergradle.json

Maven:
https://downloads.sonarsource.com/sonarqube/update/scannermaven.json

ScannerCLI:
https://downloads.sonarsource.com/sonarqube/update/scannercli.json

.Net:
https://downloads.sonarsource.com/sonarqube/update/scannermsbuild.json

Can we create a new branch and make the following changes:
- Add these links to their respective skills and specify that to get the version of the scanner/plugin it should check this link and get the latest. 
- In the agent and skills, we will need to change the web/fetch tool since this is just a tool available in vscode, i want users to be able to donwload the agent/skills and run it with any LLM so that tools have to be the basic ones every LLM will have. 

Lets make these changes and then i can test them out.



02/17
Might need to specify for project detection that it should not confirm anything with the user. That is what the prerequisites-gathering skill is for. 

The gradle-gitlab test needs to include a build.gradle example file without any sonarqube configuration for the agent to work with. 
Agent also added pipeline file and build.gradle file outside of the test workspace. 

Need to check the checkpoints, since we might need to redefine them in the tests. 
    What does the security compliance checkpoint do and how does it check it?
    what does the version currency and hwo does it check it
    What does the documentation fetches check and how it does it? 



Tested with python project, but for some reason it used v5 of the version of the action instead of the v7.




March/2
Python project test:
    GH Actions/SQ-C - Worked very nice
    