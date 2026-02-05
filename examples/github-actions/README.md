# Example GitHub Actions Workflow with SonarQube

This example demonstrates how to integrate SonarQube analysis into a GitHub Actions workflow.

## Prerequisites

1. **SonarQube Instance**: You need access to a SonarQube server or SonarCloud
2. **GitHub Secrets**: Configure these in your repository settings:
   - `SONAR_TOKEN`: Authentication token from SonarQube
   - `SONAR_HOST_URL`: URL of your SonarQube server (not needed for SonarCloud)

## How to Set Up Secrets

1. Go to your GitHub repository
2. Navigate to: **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add:
   - Name: `SONAR_TOKEN`
   - Value: Your SonarQube token
5. Repeat for `SONAR_HOST_URL` (e.g., `https://sonarqube.example.com`)

## Example Workflows

### For Node.js/TypeScript Projects

```yaml
name: SonarQube Analysis

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  sonarqube:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Shallow clones should be disabled for better analysis
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run tests with coverage
        run: npm test -- --coverage
      
      - name: SonarQube Scan
        uses: sonarsource/sonarqube-scan-action@master
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
          SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}
```

### For Java/Maven Projects

```yaml
name: SonarQube Analysis

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Set up JDK 17
        uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'
      
      - name: Cache SonarQube packages
        uses: actions/cache@v3
        with:
          path: ~/.sonar/cache
          key: ${{ runner.os }}-sonar
      
      - name: Cache Maven packages
        uses: actions/cache@v3
        with:
          path: ~/.m2
          key: ${{ runner.os }}-m2-${{ hashFiles('**/pom.xml') }}
      
      - name: Build and analyze
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
          SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}
        run: mvn -B verify org.sonarsource.scanner.maven:sonar-maven-plugin:sonar
```

## Official Documentation

For the most up-to-date information, always refer to:
- **GitHub Actions Integration**: https://docs.sonarsource.com/sonarqube/latest/devops-platform-integration/github-actions/
- **SonarQube Scan Action**: https://github.com/SonarSource/sonarqube-scan-action

## Need Help?

Use the SonarArchitect agent in VS Code:
```
@sonarqube-helper Help me set up SonarQube for GitHub Actions
```
