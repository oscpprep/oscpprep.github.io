 [
            SlackReporter,
            {
              slackOptions: {
                type: "webhook",
                webhook: process.env.SLACK_WEBHOOK_URL || "https://hooks.slack.com/services/.....",
              },
              title: 'Slack Reporter Test',
              useScenarioBasedStateCounts: true,
              uploadScreenshotOfFailedCase: true,
              notifyTestStartMessage: false,
              notifyFailedCase: true,
              notifyPassedCase: true,
              notifySkippedCase: false,
              notifyTestFinishMessage: true,
              notifyDetailResultThread: false,
              filterForDetailResults: [
                'passed',
                'failed',
                'pending',
                'skipped'
              ],
            createResultPayload: (runnerStats, stateCounts, TestStats, HookStats, SuiteStats) => {
                let specs = JSON.stringify(runnerStats.specs).split('/');
                let lastItem = specs[specs.length - 1];
                let theSpecFile = lastItem.split('.')[0];


                let jenkinsUrl = process.env.JENKINS_URL;
                let jobName = process.env.JOB_NAME;
                let buildNumber = process.env.BUILD_NUMBER;
                let allureReportUrl = `${jenkinsUrl}job/${jobName}/${buildNumber}/allure`;
                if (process.env.JENKINS_URL === undefined || process.env.JOB_NAME === undefined || process.env.BUILD_NUMBER === undefined) {
                    allureReportUrl = "";  // Allure report URL is not available. Please run this test in Jenkins to get the URL.
                }

                const payload = {
                    text: `:checkered_flag: Tested => ${theSpecFile} - :stopwatch: ${runnerStats.duration}s\n` +
                          `:white_check_mark: Passed: ${stateCounts.passed} | :x: Failed: ${stateCounts.failed}\n` +
                          `${allureReportUrl}`,
                        //   `TestStats: ${TestStats ? JSON.stringify(TestStats) : 'undefined'}\n` +
                        //   `HookStats: ${HookStats ? JSON.stringify(HookStats) : 'undefined'}\n` +
                        //   `SuiteStats: ${SuiteStats ? JSON.stringify(SuiteStats) : 'undefined'}`,
                };
                return payload;
            },
            },
        ],
