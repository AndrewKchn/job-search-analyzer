import pytest

from clients.api_client import ArbeitnowClient
from config import ARBEITNOW_API_URL


@pytest.fixture
def arbeitnow_mock_response():
    return {
        "data": [
            {
                "slug": "it-support-engineer-munich-based-447760",
                "company_name": "Bragi",
                "title": "IT Support Engineer - Munich Based",
                "description": "<p>Bragi was founded in 2013 and launched the world's first Truly Wireless Earphones in 2015 (yes, a whole 12 months before the Airpods...)</p>\n<p>Since then, we have evolved from a promising startup to a market-moving creator of innovative technology, opening the new category of Truly Wireless Earphones. Bragi transformed into a software enabler for consumer brands, focusing on scaling its technology after investing more than $90 million in software and AI.</p>\n<p>Now we are a leader in the AI headphone space, known for our smart devices that integrate seamlessly into users' lives. With a focus on innovation and user experience, we are driving the evolution of wearable technology.</p>\n<p><strong>IT Support Engineer – Munich-Based</strong></p>\n<p>We’re looking for a motivated and technically curious IT Support Engineer to join our team in Munich. If you enjoy working across different systems and helping others solve IT challenges, we’d love to meet you.</p>\n<p><strong>This role requires working in-office five days a week</strong></p>\n<h2>Tasks</h2>\n<ul>\n<li>Provide IT support for internal infrastructure and end-user systems across macOS, Windows, and Linux environments</li>\n<li>Support and administer modern SaaS platforms, enterprise applications, identity management systems, and workplace collaboration tools</li>\n<li>Troubleshoot user access, authentication, integrations, APIs, connectors, and general SaaS-related technical issues</li>\n<li>Support AI-powered workplace tools, enterprise AI integrations, and modern productivity workflows</li>\n<li>Manage IT hardware operations including device setup, onboarding/offboarding, asset tracking, shipment handling, and workstation support</li>\n<li>Support core IT infrastructure including servers, virtualization, networking, backups, datacenter operations, and office IT maintenance</li>\n<li>Maintain technical documentation, SaaS audits, IT processes, security standards, and compliance procedures aligned with DSGVO/GDPR policies</li>\n</ul>\n<h2>Requirements</h2>\n<ul>\n<li>Experience supporting SaaS platforms, enterprise applications, collaboration tools, and cloud-based workplace environments</li>\n<li>Understanding of identity and access management concepts including SSO, MFA, enterprise authentication, and user lifecycle management</li>\n<li>Experience supporting AI tools, workplace productivity platforms, and enterprise AI adoption initiatives</li>\n<li>Experience working with Windows, macOS, Linux, endpoint support, and enterprise IT environments</li>\n<li>Understanding of networking, infrastructure, virtualization, and general IT operations concepts</li>\n<li>Experience handling IT hardware, asset management, shipment coordination, employee onboarding, and office IT support</li>\n<li>Strong troubleshooting mindset with a proactive, hands-on, and service-oriented approach</li>\n</ul>\n<p><strong>Nice to have</strong></p>\n<ul>\n<li>Familiarity with GitLab runners, GitHub Actions, and CI/CD pipeline troubleshooting</li>\n<li>Interest in AI operations, SaaS security, endpoint management, and IT compliance</li>\n<li>Experience supporting modern AI workplace integrations and enterprise AI adoption</li>\n</ul>\n<h2>Benefits</h2>\n<ul>\n<li>The opportunity to help define and scale IT operations in a high-growth AI technology company</li>\n<li>Modern infrastructure and tools to support a seamless on-site work experience</li>\n<li>A collaborative and international team focused on innovation and user experience</li>\n<li>Flexible Learning &#x26; Development opportunities to support your professional growth</li>\n<li>Breakfast, lunch (Tuesday–Thursday), fresh fruits, and coffee in the office</li>\n</ul>\n<p>Find <a href=\"https://www.arbeitnow.com/\">Jobs in Germany</a> on Arbeitnow</a>",
                "remote": False,
                "url": "https://www.arbeitnow.com/jobs/companies/bragi/it-support-engineer-munich-based-447760",
                "tags": [
                    "Helpdesk"
                ],
                "job_types": [
                    "professional / experienced"
                ],
                "location": "Munich",
                "created_at": 1778252427
            }
        ]
    }


def test_fetch_page_arbeitnow_success(requests_mock, arbeitnow_mock_response):
    # Arrange
    client = ArbeitnowClient(ARBEITNOW_API_URL)
    adapter = requests_mock.get(ARBEITNOW_API_URL, json=arbeitnow_mock_response, status_code=200)

    # Act
    jobs = client.get_jobs_from_page(page_number=1)

    # Assert
    assert adapter.called
    assert adapter.call_count == 1
    assert len(jobs) == 1
    assert jobs['data'][0]['title'] == "IT Support Engineer - Munich Based"
    assert jobs['data'][0]['company_name'] == "Bragi"
    assert jobs['data'][0]['remote'] is False
