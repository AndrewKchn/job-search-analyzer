import pytest
from unittest.mock import MagicMock

from models.job_dto import JobDTO
from services.sync_service import SyncService

@pytest.fixture
def fake_job_data():
    return {
        "data": [
            {
                "slug": "werkstudentin-influencer-management-personal-branding-remote-cologne-144328",
                "company_name": "Kiwimo-Product GmbH",
                "title": "Python Developer",
                "description": "<p>Unsere Marke WhyWords unterstützt Unternehmer:innen, Expert:innen und Führungskräfte dabei, auf LinkedIn sichtbar zu werden – nicht als klassische Influencer:innen, sondern als relevante Stimmen in ihrem Fachbereich.</p>\n<p>Dafür suchen wir eine:n Werkstudent:in im Bereich Influencer Management &#x26; Personal Branding. Du arbeitest nah an unseren Kund:innen, verstehst ihre Themen, ihre Positionierung und ihre fachliche Perspektive und hilfst dabei, daraus klare Inhalte, gute Gesprächsgrundlagen und eine konsistente Personenmarke zu entwickeln.</p>\n<p>Es geht darum, unsere Kunden inhaltlich zu begleiten, Themen zu erkennen, Gedanken zu strukturieren und gemeinsam mit Redaktion und Strategie daraus starke LinkedIn-Inhalte entstehen zu lassen.</p>\n<h2>Aufgaben</h2>\n<ul>\n<li>Direkter Austausch mit Kund:innen, insbesondere in regelmäßigen Gesprächen und Sparring-Terminen</li>\n<li>Herausarbeiten von <strong>Positionierung, Tonalität, Themen und relevanten Botschaften</strong> für die LinkedIn Accounts unserer Kunden*innen</li>\n<li>Unterstützung beim Aufbau und der Weiterentwicklung von Personenmarken auf LinkedIn</li>\n<li>Strukturierung von Gedanken, Aussagen und Rohmaterial für redaktionelle Inhalte</li>\n<li>Identifikation von Content-Ideen aus Gesprächen, Notizen, Kundenkontexten und aktuellen Themen</li>\n<li>Vorbereitung und Nachbereitung von Kundengesprächen für die Redaktion</li>\n<li>Entwicklung von Content-Ideen für <strong>LinkedIn</strong> und Personal Branding</li>\n<li>Erstellung und Überarbeitung erster Textentwürfe nach redaktioneller Vorgabe</li>\n<li>Sicherstellung, dass Inhalte zur jeweiligen Person passen – in Stimme, Klarheit und Fokus</li>\n<li>Enge Zusammenarbeit mit der Redaktion</li>\n</ul>\n<h2>Qualifikation</h2>\n<ul>\n<li>Laufendes Studium, idealerweise im Master oder in einem fortgeschrittenen Bachelorstudium, z. B. in <strong>Kommunikation, Journalismus, Medien, Psychologie, Sprachwissenschaften, Marketing</strong> oder einem vergleichbaren Bereich</li>\n<li>Alternativ: vergleichbare praktische Erfahrung in Redaktion, Kommunikation, Content, Journalismus, Coaching-nahen Kontexten oder Personal Branding</li>\n<li>Sehr gutes Sprachgefühl und Freude daran, Gedanken präzise zu formulieren</li>\n<li>Interesse an Menschen, Positionierung, Kommunikation und Wirkung</li>\n<li>Fähigkeit, gut zuzuhören, Inhalte zu strukturieren und zwischen den Zeilen zu erkennen, worum es wi rklich geht</li>\n<li>Sicherer schriftlicher Ausdruck auf Deutsch</li>\n<li>Zuverlässige, eigenständige und strukturierte Arbeitsweise</li>\n<li>Souveräner Umgang mit Kund:innen im direkten Austausch</li>\n<li>Verfügbarkeit während der Vorlesungszeit im Rahmen einer Werkstudententätigkeit</li>\n</ul>\n<p><strong>Plus:</strong></p>\n<ul>\n<li>Erste Erfahrung im Agenturumfeld, in Redaktion, Social Media, Journalismus, Kommunikation oder Content Marketing</li>\n<li>Kenntnisse in LinkedIn, Personal Branding, Coaching-, Beratungs- oder Expertenkontexten</li>\n<li>Interesse an Themen wie Positionierung, Unternehmer:innen-Kommunikation und Thought Leadership</li>\n</ul>\n<h2>Benefits</h2>\n<ol>\n<li>100 % Remote-Arbeit im Homeoffice</li>\n<li>Werkstudententätigkeit mit flexibler Zeiteinteilung im Rahmen der gesetzlichen Vorgaben</li>\n<li>Planbare Zusammenarbeit mit festen Kundenterminen</li>\n<li>Eigenständige Zeiteinteilung außerhalb der Abstimmungen</li>\n<li>Klare Verantwortungsbereiche und direkter Einfluss auf Inhalte</li>\n<li>Keine unnötigen Abstimmungsschleifen, kein Mikromanagement</li>\n<li>Einblicke in Positionierung, Personal Branding, Content-Strategie und redaktionelle Prozesse</li>\n</ol>\n<p>Der Schwerpunkt der Rolle liegt weniger auf dem eigenständigen Schreiben, sondern auf der inhaltlichen Arbeit im Dialog.</p>\n<p>Wenn du gerne mit Menschen arbeitest, Gespräche führst, Themen herausarbeitest und Gedanken strukturierst, wirst du dich in dieser Rolle wiederfinden.<br>\nDas Formulieren selbst passiert im nächsten Schritt im Zusammenspiel mit der Redaktion.</p>\n<p>Hinweis: Voraussetzung für die Beschäftigung als Werkstudent:in ist eine gültige Immatrikulation an einer Hochschule oder Universität. Während der Vorlesungszeit erfolgt die Tätigkeit im Rahmen der für Werkstudent:innen geltenden Arbeitszeitgrenzen.</p>\n<p>Find more <a href=\"https://www.arbeitnow.com/english-speaking-jobs\">English Speaking Jobs in Germany</a> on Arbeitnow</a>",
                "remote": True,
                "url": "https://www.arbeitnow.com/jobs/companies/kiwimo-product-gmbh/werkstudentin-influencer-management-personal-branding-remote-cologne-144328",
                "tags": [
                    "Remote",
                    "Marketing and Communication"
                ],
                "job_types": [
                    "Working student",
                    "hilfstätigkeit / student"
                ],
                "location": "Cologne",
                "created_at": 1778437858
            }
        ],
        "links": {"next": "https://api.arbeitnow.com/jobs?page=2"}
    }
@pytest.fixture
def mock_client():
    return MagicMock()


@pytest.fixture
def mock_repository():
    return MagicMock()


def test_sync_jobs_from_page_success(mock_client, mock_repository, fake_job_data):

    # Arrange
    mock_client.get_jobs_from_page.return_value = fake_job_data
    service = SyncService(client=mock_client, repository=mock_repository)

    # Act
    service._sync_jobs_from_page(page_number=1)

    # Assert
    mock_client.get_jobs_from_page.assert_called_once_with(1)
    mock_repository.save_jobs.assert_called_once()

    passed_jobs = mock_repository.save_jobs.call_args[0][0]
    assert passed_jobs[0].title == "Python Developer"
    assert isinstance(passed_jobs[0], JobDTO)