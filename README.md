# axiadtest

Axiad Test
The test.py willl use the default config for aws.
Steps to run:

1. Create an EC2 key in your AWS - Or use the one you have already
2. Edit Params  in test.json , change KeyName ParameterValue
3. Install dependencies from Requirements.txt
4. Run python test.py

Ideally the tool is to create stack for now Other things to consider:
1. Want to add update / rollback functionality
2. Add other aws cloudformation features
3. Test the stack security and add testing strategy
4. Are keys required upfront ? we can automate that part
