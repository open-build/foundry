# Foundry
Create a Foundry and Multiple Companies Can Join

## Getting Started

First create a virtualenv
``virtualenv venv``
``source venv/bin/activate``

Then install requirements
``pip3 install -r requirements.txt``

Then Run Migrations
``python manage.py migrate``

Then Run the Test server
``python manage.py runserver``

Create a SuperUser
``python manage.py createsuperuser``

## startups datasources
Finding a public API that lists startup companies with product descriptions, current stage, and founder details can be quite useful for market research and networking. Here are a few APIs and platforms you might consider:

1. **Crunchbase API**:
   - **Description**: Crunchbase is a platform for finding business information about private and public companies. Their API provides access to data about startups, including company descriptions, funding stages, and founder details.
   - **Access**: Requires an API key which you can obtain by signing up for a developer account.
   - **Link**: [Crunchbase API](https://www.crunchbase.com/apps)

2. **AngelList API**:
   - **Description**: AngelList is a platform for startups, angel investors, and job-seekers looking to work at startups. Their API allows access to data about startups, including product descriptions and founder information.
   - **Access**: Requires an API key available upon request.
   - **Link**: [AngelList API](https://angel.co/api)

3. **Product Hunt API**:
   - **Description**: Product Hunt is a community where product enthusiasts share and discover new products. The API provides data on newly launched products, including descriptions and founder information.
   - **Access**: Requires an API key which you can obtain by signing up for a developer account.
   - **Link**: [Product Hunt API](https://api.producthunt.com/v2/docs)

4. **Mattermark API** (Note: Mattermark has been acquired, so availability may vary):
   - **Description**: Mattermark provided data on startups, including growth signals, funding rounds, and key people. This might still be accessible through other means or their acquiring company.
   - **Access**: Typically requires an API key, but it may be subject to change post-acquisition.

5. **Clearbit API**:
   - **Description**: Clearbit provides business intelligence APIs that can be used to find information about companies and people, including startups, product descriptions, and key personnel.
   - **Access**: Requires an API key which you can obtain by signing up for a developer account.
   - **Link**: [Clearbit API](https://clearbit.com/docs#company-api)

Each of these APIs requires signing up for access and often an API key. Depending on your specific needs and the depth of information you require, one of these options should be a good fit.
