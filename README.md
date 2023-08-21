# CloudTrail Accountability Reports Generator

This Python script allows you to generate accountability reports for operators by pulling CloudTrail logs for specified users and regions from AWS CloudTrail, saving the logs as CSV files, and then creating a ZIP archive of the reports.

## Prerequisites

- Python 3.x installed on your system.
- AWS CLI configured with necessary permissions.
- AWS SDK for Python (Boto3) installed.
- Input files "names" and "regions" with the list of names and regions, respectively.

## Usage on AWS CloudShell

**Access AWS CloudShell:**
- Log in to your AWS Management Console.
- Navigate to "Services" > "CloudShell" (under "Developer Tools").

**Clone the Repository:**
In the CloudShell terminal, run the following command to clone the repository to your CloudShell environment:

```bash
git clone https://github.com/tboven/AWS-Accountability.git
```
**Navigate to the Repository:**
Change the directory to the cloned repository:

```bash
cd cloudtrail-accountability
```

**Prepare Input Files:**
Edit the "names" and "regions" files to include the desired list of names and regions for which you want to generate accountability reports. You can use any text editor available in CloudShell (e.g., nano, vim, emacs).

Example "names":
```
Alice
Bob
Carol
```

Example "regions":
```
us-east-1
us-west-2
eu-west-1
```

**Run the Script:**
Run the script to generate accountability reports. Replace "Accountability.py" with the actual script filename and "YYYY-MM-DD" with the desired date:
```
bash
python3 Accountability.py --date YYYY-MM-DD
```
Omit `--date` to use the current date.
