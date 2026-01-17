"""
DPDP Act 2025 Compliance Auditor
A robust, object-oriented Python script to audit URLs against DPDP legal requirements.

Modules:
1. Consent Audit (DPDP Sec 6) - Pre-Consent Tracking Detection
2. Notice Audit (DPDP Sec 5) - Privacy Notice Requirement
3. Security Safeguards (DPDP Sec 8) - Technical Measures
4. Grievance Redressal (DPDP Sec 8) - Contact Information
"""

import time
import re
import logging
from urllib.parse import urlparse
from typing import Optional, List, Dict, Tuple
from datetime import datetime

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
# Removed: webdriver_manager - using Selenium 4 native Edge detection instead
# from webdriver_manager.microsoft import EdgeChromiumDriverManager
# from selenium.webdriver.edge.service import Service

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DPDP_Auditor:
    """
    Multi-Compliance Auditor Class
    Supports auditing against multiple data protection laws:
    - DPDP Act 2025 (India)
    - GDPR (EU - Regulation 2016/679)
    """

    def __init__(self, url: str, law: str = "DPDP"):
        """
        Initialize the auditor with a target URL and law to audit against
        
        Args:
            url: Target website URL to audit
            law: Which law to audit against ("DPDP" or "GDPR"). Defaults to "DPDP"
        """
        self.url = self._normalize_url(url)
        self.domain = urlparse(self.url).netloc
        self.driver = None
        self.privacy_policy_url = None
        self.privacy_policy_text = None  # Cache policy text to avoid repeated fetches
        self.law = law.upper()  # Store as uppercase for consistency
        
        # Initialize audit report structure
        if self.law == "GDPR":
            self.audit_report = {
                'gdpr_1': [],  # Strict Consent (Article 6)
                'gdpr_2': [],  # Governance (Article 37)
                'gdpr_3': [],  # Rights Bundle (Articles 15-21)
                'gdpr_4': [],  # Transparency & Complaints (Art 77)
                'gdpr_5': []   # International Transfers (Art 44-46)
            }
        else:  # Default DPDP
            self.audit_report = {
                'module_1': [],  # Consent Audit
                'module_2': [],  # Notice Audit
                'module_3': [],  # Security Safeguards
                'module_4': [],  # Grievance Redressal
                'module_5': [],  # Breach Notification (Rule 7)
                'module_6': [],  # Children's Data (Section 9 & Rule 10)
                'module_7': []   # Data Retention (Rule 8)
            }
        logger.info(f"Auditor initialized for {self.law} compliance: {self.url}")

    def _normalize_url(self, url: str) -> str:
        """Ensure URL has proper protocol"""
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        return url

    def _setup_driver(self) -> webdriver.Edge:
        """
        Setup Selenium WebDriver (Native Mode)
        This skips the webdriver_manager download check and uses your installed Edge directly.
        
        Returns:
            Configured Edge WebDriver instance
        """
        try:
            edge_options = Options()
            
            # Anti-Detection: Set real User-Agent
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
            edge_options.add_argument(f'user-agent={user_agent}')
            
            # Anti-Detection: Disable automation flags
            edge_options.add_argument('--disable-blink-features=AutomationControlled')
            edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            edge_options.add_experimental_option('useAutomationExtension', False)
            
            # Stability options
            edge_options.add_argument('--no-sandbox')
            edge_options.add_argument('--disable-dev-shm-usage')
            edge_options.add_argument('--disable-gpu')
            
            # Native Mode: Selenium 4 finds Edge automatically (no internet needed)
            driver = webdriver.Edge(options=edge_options)
            
            logger.info("WebDriver setup successful (Native Edge Mode)")
            return driver
            
        except Exception as e:
            logger.error(f"Failed to setup WebDriver: {str(e)}")
            print(f"\n[CRITICAL ERROR] Could not open Edge Browser.")
            print("Tip: Make sure you have Microsoft Edge installed.")
            raise

    def _get_policy_text(self) -> str:
        """
        Smart Fetcher: Intelligently retrieves Privacy Policy text.
        
        Strategy:
        1. Check if privacy_policy_url is already set (manual override or auto-discovered)
        2. First try: Selenium browser (respects page rendering, JS execution)
        3. Fallback: Requests library (faster, lighter, often bypasses blocks)
        4. Return cached text if already fetched
        
        Returns:
            Policy text as string (lowercase for case-insensitive searching)
        """
        # Return cached text if we already have it
        if self.privacy_policy_text:
            logger.info("Using cached privacy policy text")
            return self.privacy_policy_text

        if not self.privacy_policy_url:
            logger.warning("No privacy policy URL available")
            return ""

        logger.info(f"Fetching Privacy Policy from: {self.privacy_policy_url}")

        # Attempt 1: Selenium Browser (Full rendering)
        try:
            self.driver.set_page_load_timeout(30)
            self.driver.get(self.privacy_policy_url)
            time.sleep(3)  # Allow scripts to execute
            self.privacy_policy_text = self.driver.find_element(By.TAG_NAME, "body").text.lower()
            logger.info(f"✓ Successfully fetched policy via Selenium ({len(self.privacy_policy_text)} chars)")
            return self.privacy_policy_text
        except TimeoutException:
            logger.warning("Selenium timed out (likely being blocked). Attempting fallback...")
        except Exception as e:
            logger.warning(f"Selenium failed ({type(e).__name__}: {str(e)}). Attempting fallback...")

        # Attempt 2: Requests Library (Lightweight, often bypasses blocks)
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            response = requests.get(self.privacy_policy_url, headers=headers, timeout=15, verify=False)
            if response.status_code == 200:
                # Extract text from HTML (simple method - keeps body content)
                self.privacy_policy_text = response.text.lower()
                logger.info(f"✓ Successfully fetched policy via Requests fallback ({len(self.privacy_policy_text)} chars)")
                return self.privacy_policy_text
            else:
                logger.error(f"Requests returned status {response.status_code}")
        except Exception as e:
            logger.error(f"Fallback requests also failed: {type(e).__name__}: {str(e)}")

        logger.error("Could not fetch privacy policy via any method")
        return ""

    def module_1_consent_audit(self) -> None:
        """
        Module 1: Consent Audit (DPDP Sec 6 - Pre-Consent Tracking)
        
        Logic:
        - Visit URL without accepting cookies
        - Wait 5 seconds for scripts to load
        - Extract and filter cookies
        - Flag 3rd party trackers and pre-consent tracking
        """
        logger.info("=== MODULE 1: CONSENT AUDIT (DPDP Sec 6) ===")
        
        try:
            self.driver.get(self.url)
            logger.info(f"Navigated to: {self.url}")
            
            # Wait 15 seconds for ad scripts to load and set cookies
            time.sleep(15)
            
            # Extract all cookies without clicking Accept
            all_cookies = self.driver.get_cookies()
            
            if not all_cookies:
                self.audit_report['module_1'].append({
                    'status': 'PASS',
                    'message': 'Sec 6(1): No tracking cookies found on initial load'
                })
                logger.info("✓ No cookies set before consent")
                return
            
            # Essential cookie keywords to ignore (legitimate, non-tracking)
            essential_keywords = ['session', 'id', 'csrf', 'auth', 'token', 'secure', 'httponly']
            
            # Known tracker signatures - catches "stealth trackers" hidden on first-party domain
            # These are ad-tech and analytics cookies that should require explicit consent
            tracker_signatures = [
                '_ga', '_gid',          # Google Analytics
                '_fbp', '_fbc',         # Facebook
                '_uetsid',              # Microsoft UET
                '_uetvid',              # Microsoft UET
                'adsid',                # Google Ads
                'doubleclick',          # Google DoubleClick
                'rubicon',              # Rubicon Project
                'criteo',               # Criteo
                'amazon_aid',           # Amazon Ads
                'ttd_uuid',             # The Trade Desk
                'dpm',                  # Dianomi
                'mage',                 # Magnolia
                'c3',                   # C3 Metrics
                'kenshoo',              # Kenshoo
                'affectv',              # AffectV
                'bluekai'               # BlueKai (Oracle)
            ]
            
            third_party_trackers = []
            
            for cookie in all_cookies:
                cookie_name = cookie.get('name', '').lower()
                cookie_domain = cookie.get('domain', '').lower()
                
                # Check if cookie is essential (legitimate, non-tracking)
                is_essential = any(keyword in cookie_name for keyword in essential_keywords)
                
                # Check if cookie is 3rd party (domain different from target)
                is_external_domain = not (self.domain in cookie_domain or cookie_domain.replace('www.', '') in self.domain)
                
                # Check if cookie matches known tracker signature (stealth tracker detection)
                is_known_tracker = any(sig in cookie_name for sig in tracker_signatures)
                
                # Flag if it's either external OR a known tracker (and not essential)
                if not is_essential and (is_external_domain or is_known_tracker):
                    tracker_type = 'Known Tracker' if is_known_tracker else 'External Domain'
                    third_party_trackers.append({
                        'name': cookie.get('name'),
                        'domain': cookie_domain,
                        'type': tracker_type
                    })
                    logger.warning(f"Tracker Found [{tracker_type}]: {cookie.get('name')} from {cookie_domain}")
            
            if third_party_trackers:
                self.audit_report['module_1'].append({
                    'status': 'VIOLATION',
                    'message': f'Sec 6(1): Data processed without consent - {len(third_party_trackers)} unauthorized trackers found',
                    'details': third_party_trackers
                })
                print(f"\n[VIOLATION] Sec 6(1): Data processed without consent")
                print(f"  └─ Found {len(third_party_trackers)} unauthorized tracking cookies:")
                for tracker in third_party_trackers:
                    print(f"     • {tracker['name']} [{tracker['type']}] (from {tracker['domain']})")
            else:
                self.audit_report['module_1'].append({
                    'status': 'PASS',
                    'message': 'Sec 6(1): No unauthorized tracking cookies found before consent'
                })
                print("[PASS] Sec 6(1): No unauthorized pre-consent tracking detected")
                
        except WebDriverException as e:
            logger.error(f"WebDriver error in Module 1: {str(e)}")
            self.audit_report['module_1'].append({
                'status': 'ERROR',
                'message': f'Failed to audit consent: {str(e)}'
            })
        except Exception as e:
            logger.error(f"Unexpected error in Module 1: {str(e)}")
            self.audit_report['module_1'].append({
                'status': 'ERROR',
                'message': f'Consent audit failed: {str(e)}'
            })

    def module_2_notice_audit(self) -> None:
        """
        Module 2: Notice Audit (DPDP Sec 5 - Notice Requirement)
        
        Logic:
        - Scan homepage HTML for privacy-related links
        - Look for: "Privacy", "Policy", "Notice", "Data"
        - Save Privacy Policy URL for Module 4
        """
        logger.info("=== MODULE 2: NOTICE AUDIT (DPDP Sec 5) ===")
        
        try:
            # Get page source
            page_source = self.driver.page_source
            
            # Look for privacy policy links - enhanced with UK/academic keywords
            privacy_keywords = [
                'privacy', 'policy', 'notice', 'data protection', 'personal data',
                'privacy statement', 'gdpr', 'cookie', 'data policy',
                'legal', 'terms', 'terms and conditions', 'data notice',
                'information governance', 'records management'  # UK/academic specific
            ]
            
            # Find all links in the page
            links = self.driver.find_elements(By.XPATH, "//a[@href]")
            
            found_privacy_link = False
            
            for link in links:
                try:
                    link_text = link.text.lower()
                    link_href = link.get_attribute('href')
                    
                    # Check if link contains privacy-related keywords
                    if any(keyword in link_text for keyword in privacy_keywords):
                        # Make URL absolute if relative
                        if link_href:
                            if link_href.startswith('http'):
                                self.privacy_policy_url = link_href
                            elif link_href.startswith('/'):
                                base_url = f"{urlparse(self.url).scheme}://{urlparse(self.url).netloc}"
                                self.privacy_policy_url = base_url + link_href
                            else:
                                # Handle relative URLs
                                base_url = f"{urlparse(self.url).scheme}://{urlparse(self.url).netloc}"
                                self.privacy_policy_url = base_url + '/' + link_href
                            
                            found_privacy_link = True
                            logger.info(f"Privacy Policy URL found: {self.privacy_policy_url}")
                            break
                except Exception as e:
                    logger.debug(f"Error processing link: {str(e)}")
                    continue
            
            if found_privacy_link:
                self.audit_report['module_2'].append({
                    'status': 'PASS',
                    'message': 'Sec 5(1): Privacy Notice link found',
                    'url': self.privacy_policy_url
                })
                print(f"\n[PASS] Sec 5(1): Privacy Notice link found")
                print(f"  └─ URL: {self.privacy_policy_url}")
            else:
                self.audit_report['module_2'].append({
                    'status': 'VIOLATION',
                    'message': 'Sec 5(1): No Privacy Notice link found'
                })
                print(f"\n[VIOLATION] Sec 5(1): No Privacy Notice link found")
                
        except Exception as e:
            logger.error(f"Error in Module 2: {str(e)}")
            self.audit_report['module_2'].append({
                'status': 'ERROR',
                'message': f'Notice audit failed: {str(e)}'
            })

    def module_3_security_safeguards(self) -> None:
        """
        Module 3: Security Safeguards (DPDP Sec 8 - Technical Measures)
        
        Logic:
        - Fetch HTTP headers using requests
        - Check for: Strict-Transport-Security, X-Frame-Options, X-Content-Type-Options
        - Flag missing headers as risks
        """
        logger.info("=== MODULE 3: SECURITY SAFEGUARDS (DPDP Sec 8) ===")
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(self.url, headers=headers, timeout=10, allow_redirects=True)
            response_headers = response.headers
            
            logger.info(f"HTTP Status: {response.status_code}")
            
            # Required security headers
            required_headers = {
                'Strict-Transport-Security': 'HSTS',
                'X-Frame-Options': 'Clickjacking Protection',
                'X-Content-Type-Options': 'MIME Type Sniffing Protection'
            }
            
            missing_headers = []
            present_headers = []
            
            for header_name, description in required_headers.items():
                if header_name in response_headers:
                    present_headers.append(f"{header_name}: {response_headers[header_name][:50]}")
                    logger.info(f"✓ {header_name} present")
                else:
                    missing_headers.append((header_name, description))
                    logger.warning(f"✗ {header_name} missing")
            
            if missing_headers:
                self.audit_report['module_3'].append({
                    'status': 'RISK',
                    'message': f'Sec 8(5): Missing {len(missing_headers)} security headers',
                    'missing_headers': missing_headers,
                    'present_headers': present_headers
                })
                print(f"\n[RISK] Sec 8(5): Missing Security Headers")
                for header, desc in missing_headers:
                    print(f"  ✗ {header} ({desc})")
                if present_headers:
                    print(f"  ✓ Found:")
                    for header in present_headers:
                        print(f"     • {header}")
            else:
                self.audit_report['module_3'].append({
                    'status': 'PASS',
                    'message': 'Sec 8(5): All required security headers present',
                    'headers': present_headers
                })
                print(f"\n[PASS] Sec 8(5): All required security headers present")
                for header in present_headers:
                    print(f"  ✓ {header}")
                    
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error in Module 3: {str(e)}")
            self.audit_report['module_3'].append({
                'status': 'ERROR',
                'message': f'Could not fetch security headers: {str(e)}'
            })
        except Exception as e:
            logger.error(f"Error in Module 3: {str(e)}")
            self.audit_report['module_3'].append({
                'status': 'ERROR',
                'message': f'Security audit failed: {str(e)}'
            })

    def module_4_grievance_redressal(self) -> None:
        """
        Module 4: Grievance Redressal (DPDP Sec 8)
        Updated to use cached policy_text to avoid timeouts.
        """
        logger.info("=== MODULE 4: GRIEVANCE REDRESSAL (DPDP Sec 8) ===")
        
        # 1. Get the text (Cached or New)
        policy_text = self._get_policy_text()
        
        if not policy_text:
            logger.warning("No Privacy Policy content available (Module 2 failed or Fetch failed)")
            self.audit_report['module_4'].append({
                'status': 'SKIP',
                'message': 'Sec 8(9): Skipped - Could not fetch Policy text'
            })
            print(f"\n[SKIP] Sec 8(9): Privacy Policy not accessible - cannot verify grievance details")
            return
        
        try:
            # 2. Extract emails from the TEXT (not page_source)
            email_pattern = r'[\w\.-]+@[\w\.-]+'
            emails = re.findall(email_pattern, policy_text)
            
            # Remove duplicates
            emails = list(set(emails))
            
            logger.info(f"Found {len(emails)} email addresses")
            
            # Context keywords
            grievance_keywords = ['grievance', 'officer', 'dpo', 'contact', 'support', 'complaint', 'redressal']
            
            grievance_emails = []
            
            if emails:
                for email in emails:
                    # 3. FIX IS HERE: Use 'policy_text' instead of 'page_source'
                    for keyword in grievance_keywords:
                        if keyword in policy_text:
                            if self._is_email_near_keyword(policy_text, email.lower(), keyword):
                                grievance_emails.append(email)
                                logger.info(f"Grievance contact found: {email}")
                                break
            
            if grievance_emails:
                self.audit_report['module_4'].append({
                    'status': 'PASS',
                    'message': 'Sec 8(9): Grievance Officer contact details found',
                    'emails': grievance_emails
                })
                print(f"\n[PASS] Sec 8(9): Grievance Officer contact details found")
                for email in grievance_emails:
                    print(f"  ✓ Contact: {email}")
            elif emails:
                self.audit_report['module_4'].append({
                    'status': 'RISK',
                    'message': 'Sec 8(9): Email addresses found but grievance context unclear',
                    'emails': emails[:5]
                })
                print(f"\n[RISK] Sec 8(9): Email addresses found but grievance context unclear")
                print(f"  └─ Found emails: {', '.join(emails[:3])}")
            else:
                self.audit_report['module_4'].append({
                    'status': 'VIOLATION',
                    'message': 'Sec 8(9): No Grievance Officer details found'
                })
                print(f"\n[VIOLATION] Sec 8(9): No Grievance Officer contact details found")

        except Exception as e:
            logger.error(f"Error in Module 4: {str(e)}")
            self.audit_report['module_4'].append({
                'status': 'ERROR',
                'message': f'Grievance audit failed: {str(e)}'
            })

    def _is_email_near_keyword(self, page_text: str, email: str, keyword: str, distance: int = 200) -> bool:
        """
        Check if email appears near a keyword in the page text
        
        Args:
            page_text: Full page text in lowercase
            email: Email address to search for
            keyword: Keyword to check proximity
            distance: Character distance threshold
            
        Returns:
            True if email is near keyword, False otherwise
        """
        try:
            email_pos = page_text.find(email)
            keyword_pos = page_text.find(keyword)
            
            if email_pos == -1 or keyword_pos == -1:
                return False
            
            return abs(email_pos - keyword_pos) <= distance
        except Exception:
            return False

    def module_5_breach_notification(self) -> None:
        """
        Module 5: Breach Notification (DPDP Rule 7)
        
        Requirement: Companies must notify users of data breaches without delay
        and notify Data Protection Board within 72 hours
        
        Logic: Scan Privacy Policy for breach notification keywords using smart fetcher
        """
        logger.info("=== MODULE 5: BREACH NOTIFICATION (DPDP Rule 7) ===")
        
        if not self.privacy_policy_url:
            logger.warning("No Privacy Policy URL available (Module 2 failed)")
            self.audit_report['module_5'].append({
                'status': 'SKIP',
                'message': 'Rule 7: Skipped - No Privacy Policy URL found'
            })
            print(f"\n[SKIP] Rule 7: Privacy Policy not accessible - cannot verify breach notification")
            return
        
        try:
            # Use smart fetcher to get policy text (cached)
            policy_text = self._get_policy_text()
            
            if not policy_text:
                self.audit_report['module_5'].append({
                    'status': 'ERROR',
                    'message': 'Rule 7: Could not fetch Privacy Policy for analysis'
                })
                logger.error("Could not fetch privacy policy text")
                return
            
            # Keywords for breach notification compliance
            breach_keywords = ['breach', 'notification', '72 hours', 'incident', 'data breach', 
                              'unauthorized access', 'notify', 'disclosure', 'security incident']
            
            found_keywords = []
            for keyword in breach_keywords:
                if keyword in policy_text:
                    found_keywords.append(keyword)
                    logger.info(f"Found breach keyword: {keyword}")
            
            if found_keywords:
                self.audit_report['module_5'].append({
                    'status': 'PASS',
                    'message': f'Rule 7: Breach notification policy found',
                    'keywords': found_keywords
                })
                print(f"\n[PASS] Rule 7: Breach notification policy documented")
                print(f"  ✓ Keywords found: {', '.join(set(found_keywords))}")
            else:
                self.audit_report['module_5'].append({
                    'status': 'VIOLATION',
                    'message': 'Rule 7: No breach notification policy mentioned'
                })
                print(f"\n[VIOLATION] Rule 7: No breach notification policy found")
                print(f"  └─ Policy must include: Breach, Notification, 72 hours, Incident")
                
        except Exception as e:
            logger.error(f"Error in Module 5: {str(e)}")
            self.audit_report['module_5'].append({
                'status': 'ERROR',
                'message': f'Breach notification audit failed: {str(e)}'
            })

    def module_6_children_data(self) -> None:
        """
        Module 6: Children's Data Protection (DPDP Section 9 & Rule 10)
        
        Requirement: Special protection for children's data
        Rule 10 mandates "Verifiable Parental Consent"
        
        Logic: Scan Privacy Policy for children/minors/parental consent keywords using smart fetcher
        """
        logger.info("=== MODULE 6: CHILDREN'S DATA PROTECTION (DPDP Section 9 & Rule 10) ===")
        
        if not self.privacy_policy_url:
            logger.warning("No Privacy Policy URL available (Module 2 failed)")
            self.audit_report['module_6'].append({
                'status': 'SKIP',
                'message': 'Section 9 & Rule 10: Skipped - No Privacy Policy URL found'
            })
            print(f"\n[SKIP] Section 9 & Rule 10: Privacy Policy not accessible")
            return
        
        try:
            # Use smart fetcher to get policy text (cached)
            policy_text = self._get_policy_text()
            
            if not policy_text:
                self.audit_report['module_6'].append({
                    'status': 'ERROR',
                    'message': 'Section 9 & Rule 10: Could not fetch Privacy Policy for analysis'
                })
                logger.error("Could not fetch privacy policy text")
                return
            
            # Keywords for children's data protection
            children_keywords = ['child', 'minor', 'parent', 'guardian', 'age verification', 
                                'parental consent', 'verifiable consent', 'under 18', 'juvenile']
            
            found_keywords = []
            for keyword in children_keywords:
                if keyword in policy_text:
                    found_keywords.append(keyword)
                    logger.info(f"Found children's data keyword: {keyword}")
            
            if found_keywords:
                self.audit_report['module_6'].append({
                    'status': 'PASS',
                    'message': f'Section 9 & Rule 10: Children\'s data protection policy found',
                    'keywords': found_keywords
                })
                print(f"\n[PASS] Section 9 & Rule 10: Children's data protection policy documented")
                print(f"  ✓ Keywords found: {', '.join(set(found_keywords))}")
            else:
                self.audit_report['module_6'].append({
                    'status': 'VIOLATION',
                    'message': 'Section 9 & Rule 10: No children\'s data protection policy mentioned'
                })
                print(f"\n[VIOLATION] Section 9 & Rule 10: No children's data protection found")
                print(f"  └─ Policy must include: Child, Minor, Parent, Guardian, Parental Consent")
                
        except Exception as e:
            logger.error(f"Error in Module 6: {str(e)}")
            self.audit_report['module_6'].append({
                'status': 'ERROR',
                'message': f'Children\'s data audit failed: {str(e)}'
            })

    def module_7_data_retention(self) -> None:
        """
        Module 7: Data Retention Policy (DPDP Rule 8)
        
        Requirement: Data must be erased when no longer needed
        Rule 8(3) requires minimum 1-year log retention
        
        Logic: Scan Privacy Policy for data retention/deletion keywords using smart fetcher
        """
        logger.info("=== MODULE 7: DATA RETENTION (DPDP Rule 8) ===")
        
        if not self.privacy_policy_url:
            logger.warning("No Privacy Policy URL available (Module 2 failed)")
            self.audit_report['module_7'].append({
                'status': 'SKIP',
                'message': 'Rule 8: Skipped - No Privacy Policy URL found'
            })
            print(f"\n[SKIP] Rule 8: Privacy Policy not accessible - cannot verify retention policy")
            return
        
        try:
            # Use smart fetcher to get policy text (cached)
            policy_text = self._get_policy_text()
            
            if not policy_text:
                self.audit_report['module_7'].append({
                    'status': 'ERROR',
                    'message': 'Rule 8: Could not fetch Privacy Policy for analysis'
                })
                logger.error("Could not fetch privacy policy text")
                return
            
            # Keywords for data retention compliance
            retention_keywords = ['retention', 'delete', 'erase', 'removal', '1 year', 'one year',
                                 'log retention', 'data deletion', 'purge', 'destroy']
            
            found_keywords = []
            for keyword in retention_keywords:
                if keyword in policy_text:
                    found_keywords.append(keyword)
                    logger.info(f"Found retention keyword: {keyword}")
            
            if found_keywords:
                self.audit_report['module_7'].append({
                    'status': 'PASS',
                    'message': f'Rule 8: Data retention policy documented',
                    'keywords': found_keywords
                })
                print(f"\n[PASS] Rule 8: Data retention policy documented")
                print(f"  ✓ Keywords found: {', '.join(set(found_keywords))}")
            else:
                self.audit_report['module_7'].append({
                    'status': 'VIOLATION',
                    'message': 'Rule 8: No data retention/deletion policy mentioned'
                })
                print(f"\n[VIOLATION] Rule 8: No data retention policy found")
                print(f"  └─ Policy must include: Retention, Delete, Erase, 1 year, Log retention")
                
        except Exception as e:
            logger.error(f"Error in Module 7: {str(e)}")
            self.audit_report['module_7'].append({
                'status': 'ERROR',
                'message': f'Data retention audit failed: {str(e)}'
            })

    def run_audit(self) -> Dict:
        """
        Execute complete compliance audit (DPDP or GDPR)
        
        Returns:
            Dictionary containing audit results
        """
        if self.law == "GDPR":
            return self._audit_gdpr()
        else:
            return self._audit_dpdp()

    def _audit_dpdp(self) -> Dict:
        """Execute complete DPDP compliance audit (all 7 modules)"""
        print("\n" + "="*70)
        print("DPDP ACT 2025 COMPLIANCE AUDITOR")
        print(f"Target URL: {self.url}")
        print("="*70)
        
        try:
            # Initialize WebDriver
            self.driver = self._setup_driver()
            
            # Run all 7 modules
            self.module_1_consent_audit()
            self.module_2_notice_audit()
            self.module_3_security_safeguards()
            self.module_4_grievance_redressal()
            self.module_5_breach_notification()
            self.module_6_children_data()
            self.module_7_data_retention()
            
            # Generate final report
            self._generate_report()
            
            # Generate PDF report
            pdf_file = self._generate_pdf_report()
            print(f"\n📄 PDF Report saved: {pdf_file}")
            
            return self.audit_report
            
        except Exception as e:
            logger.error(f"Fatal error during DPDP audit: {str(e)}")
            print(f"\n[ERROR] Audit failed: {str(e)}")
            return self.audit_report
            
        finally:
            # Cleanup
            if self.driver:
                try:
                    self.driver.quit()
                    logger.info("WebDriver closed successfully")
                except Exception as e:
                    logger.warning(f"Error closing WebDriver: {str(e)}")

    def _audit_gdpr(self) -> Dict:
        """Execute complete GDPR compliance audit (5 pillars)"""
        print("\n" + "="*70)
        print("GDPR (EU 2016/679) COMPLIANCE AUDITOR")
        print(f"Target URL: {self.url}")
        print("="*70)
        
        try:
            # Initialize WebDriver
            self.driver = self._setup_driver()
            
            # Run all 5 GDPR pillars
            self._check_gdpr_pillar_1_consent()
            self._check_gdpr_pillar_2_governance()
            self._check_gdpr_pillar_3_rights()
            self._check_gdpr_pillar_4_transparency()
            self._check_gdpr_pillar_5_transfers()
            
            # Generate final report
            self._generate_report()
            
            # Generate PDF report
            pdf_file = self._generate_pdf_report()
            print(f"\n📄 PDF Report saved: {pdf_file}")
            
            return self.audit_report
            
        except Exception as e:
            logger.error(f"Fatal error during GDPR audit: {str(e)}")
            print(f"\n[ERROR] GDPR audit failed: {str(e)}")
            return self.audit_report
            
        finally:
            # Cleanup
            if self.driver:
                try:
                    self.driver.quit()
                    logger.info("WebDriver closed successfully")
                except Exception as e:
                    logger.warning(f"Error closing WebDriver: {str(e)}")

    # ===== GDPR COMPLIANCE CHECKS (5 PILLARS) =====

    def _check_gdpr_pillar_1_consent(self) -> None:
        """
        GDPR Pillar 1: Strict Consent (Article 6)
        
        Requirement: Consent must be obtained BEFORE any tracking/processing
        
        Check: Re-use DPDP cookie checking logic - if trackers load before 
               user accepts cookies, it's a VIOLATION
        """
        logger.info("=== GDPR PILLAR 1: STRICT CONSENT (Article 6) ===")
        
        try:
            self.driver.get(self.url)
            logger.info(f"Navigated to: {self.url}")
            
            # Wait 15 seconds for ad scripts to load and set cookies
            time.sleep(15)
            
            # Extract all cookies without clicking Accept
            all_cookies = self.driver.get_cookies()
            
            if not all_cookies:
                self.audit_report['gdpr_1'].append({
                    'status': 'PASS',
                    'message': 'Article 6: No tracking cookies found before consent - COMPLIANT'
                })
                logger.info("✓ No cookies set before consent")
                print("[PASS] Article 6: Strict Consent - No pre-consent tracking detected")
                return
            
            # Essential cookie keywords to ignore (legitimate, non-tracking)
            essential_keywords = ['session', 'id', 'csrf', 'auth', 'token', 'secure', 'httponly', 'language', 'preference']
            
            # Known tracker signatures
            tracker_signatures = [
                '_ga', '_gid',          # Google Analytics
                '_fbp', '_fbc',         # Facebook
                '_uetsid',              # Microsoft UET
                '_uetvid',              # Microsoft UET
                'adsid',                # Google Ads
                'doubleclick',          # Google DoubleClick
                'rubicon',              # Rubicon Project
                'criteo',               # Criteo
                'amazon_aid',           # Amazon Ads
                'ttd_uuid',             # The Trade Desk
                'dpm',                  # Dianomi
                'c3',                   # C3 Metrics
                'kenshoo',              # Kenshoo
                'affectv',              # AffectV
                'bluekai'               # BlueKai (Oracle)
            ]
            
            third_party_trackers = []
            
            for cookie in all_cookies:
                cookie_name = cookie.get('name', '').lower()
                cookie_domain = cookie.get('domain', '').lower()
                
                # Check if cookie is essential
                is_essential = any(keyword in cookie_name for keyword in essential_keywords)
                
                # Check if cookie is 3rd party
                is_external_domain = not (self.domain in cookie_domain or cookie_domain.replace('www.', '') in self.domain)
                
                # Check if cookie matches known tracker signature
                is_known_tracker = any(sig in cookie_name for sig in tracker_signatures)
                
                # Flag if it's either external OR a known tracker (and not essential)
                if not is_essential and (is_external_domain or is_known_tracker):
                    tracker_type = 'Known Tracker' if is_known_tracker else 'External Domain'
                    third_party_trackers.append({
                        'name': cookie.get('name'),
                        'domain': cookie_domain,
                        'type': tracker_type
                    })
                    logger.warning(f"Tracker Found [{tracker_type}]: {cookie.get('name')} from {cookie_domain}")
            
            if third_party_trackers:
                self.audit_report['gdpr_1'].append({
                    'status': 'VIOLATION',
                    'message': f'Article 6: Data processed without consent - {len(third_party_trackers)} unauthorized trackers found',
                    'details': third_party_trackers,
                    'severity': 'CRITICAL'
                })
                print(f"\n[VIOLATION] Article 6: STRICT CONSENT VIOLATED - Trackers loaded before consent!")
                print(f"  └─ Found {len(third_party_trackers)} unauthorized tracking cookies:")
                for tracker in third_party_trackers:
                    print(f"     • {tracker['name']} [{tracker['type']}] (from {tracker['domain']})")
            else:
                self.audit_report['gdpr_1'].append({
                    'status': 'PASS',
                    'message': 'Article 6: No unauthorized tracking cookies found before consent'
                })
                print("[PASS] Article 6: Strict Consent - COMPLIANT")
                
        except WebDriverException as e:
            logger.error(f"WebDriver error in GDPR Pillar 1: {str(e)}")
            self.audit_report['gdpr_1'].append({
                'status': 'ERROR',
                'message': f'Failed to audit consent: {str(e)}'
            })
        except Exception as e:
            logger.error(f"Error in GDPR Pillar 1: {str(e)}")
            self.audit_report['gdpr_1'].append({
                'status': 'ERROR',
                'message': f'Consent audit failed: {str(e)}'
            })

    def _check_gdpr_pillar_2_governance(self) -> None:
        """
        GDPR Pillar 2: Governance (Article 37)
        
        Requirement: Organizations should appoint a Data Protection Officer (DPO)
        and document their role.
        
        Check: Search policy for "Data Protection Officer" or "DPO"
               If missing: RISK (-10 points)
        """
        logger.info("=== GDPR PILLAR 2: GOVERNANCE (Article 37 - DPO) ===")
        
        if not self.privacy_policy_url:
            logger.warning("No Privacy Policy URL available (Module 2 failed)")
            self.audit_report['gdpr_2'].append({
                'status': 'SKIP',
                'message': 'Article 37: Skipped - Privacy Policy not accessible'
            })
            print(f"\n[SKIP] Article 37: Privacy Policy not accessible - cannot verify DPO")
            return
        
        try:
            # Get policy text
            policy_text = self._get_policy_text()
            
            if not policy_text:
                self.audit_report['gdpr_2'].append({
                    'status': 'ERROR',
                    'message': 'Article 37: Could not fetch Privacy Policy for analysis'
                })
                logger.error("Could not fetch privacy policy text")
                return
            
            # Search for DPO keywords
            dpo_keywords = ['data protection officer', 'dpo', 'appointed dpo', 'designate', 'responsible']
            
            found_dpo = False
            for keyword in dpo_keywords:
                if keyword in policy_text:
                    found_dpo = True
                    logger.info(f"Found DPO reference: {keyword}")
                    break
            
            if found_dpo:
                self.audit_report['gdpr_2'].append({
                    'status': 'PASS',
                    'message': 'Article 37: Data Protection Officer (DPO) mentioned in policy'
                })
                print(f"\n[PASS] Article 37: Data Protection Officer governance - DOCUMENTED")
            else:
                self.audit_report['gdpr_2'].append({
                    'status': 'RISK',
                    'message': 'Article 37: Data Protection Officer (DPO) not mentioned',
                    'score_deduction': -10,
                    'recommendation': 'Clarify DPO appointment or responsibility delegation'
                })
                print(f"\n[RISK] Article 37: Data Protection Officer not mentioned (-10 points)")
                print(f"  └─ Best Practice: Clearly document DPO appointment/contact")
                
        except Exception as e:
            logger.error(f"Error in GDPR Pillar 2: {str(e)}")
            self.audit_report['gdpr_2'].append({
                'status': 'ERROR',
                'message': f'Governance audit failed: {str(e)}'
            })

    def _check_gdpr_pillar_3_rights(self) -> None:
        """
        GDPR Pillar 3: The "Rights Bundle" (Articles 15-21)
        
        Requirement: Policy MUST explicitly mention ALL 6 rights:
        - Right of Access (Art 15)
        - Right to Rectification (Art 16)
        - Right to Erasure / "Be Forgotten" (Art 17)
        - Right to Restriction (Art 18)
        - Right to Portability (Art 20)
        - Right to Object (Art 21)
        
        Scoring: -5 points for each missing right
        """
        logger.info("=== GDPR PILLAR 3: RIGHTS BUNDLE (Articles 15-21) ===")
        
        if not self.privacy_policy_url:
            logger.warning("No Privacy Policy URL available")
            self.audit_report['gdpr_3'].append({
                'status': 'SKIP',
                'message': 'Articles 15-21: Skipped - Privacy Policy not accessible'
            })
            print(f"\n[SKIP] Articles 15-21: Privacy Policy not accessible - cannot verify rights")
            return
        
        try:
            # Get policy text
            policy_text = self._get_policy_text()
            
            if not policy_text:
                self.audit_report['gdpr_3'].append({
                    'status': 'ERROR',
                    'message': 'Articles 15-21: Could not fetch Privacy Policy for analysis'
                })
                logger.error("Could not fetch privacy policy text")
                return
            
            # Define the 6 rights with their keywords
            rights = {
                'Right of Access (Art 15)': ['access', 'right of access', 'access to data'],
                'Right to Rectification (Art 16)': ['rectif', 'correct', 'amend', 'update information'],
                'Right to Erasure (Art 17)': ['right to be forgotten', 'erasure', 'delete', 'erase', 'removal'],
                'Right to Restriction (Art 18)': ['restrict', 'restriction of processing', 'suspend'],
                'Right to Portability (Art 20)': ['data portab', 'portable', 'receive data', 'machine-readable'],
                'Right to Object (Art 21)': ['right to object', 'objection', 'reject processing']
            }
            
            found_rights = []
            missing_rights = []
            
            for right_name, keywords in rights.items():
                found = False
                for keyword in keywords:
                    if keyword in policy_text:
                        found = True
                        found_rights.append(right_name)
                        logger.info(f"Found: {right_name}")
                        break
                
                if not found:
                    missing_rights.append(right_name)
                    logger.warning(f"Missing: {right_name}")
            
            # Calculate score deduction
            score_deduction = len(missing_rights) * -5
            
            if missing_rights:
                self.audit_report['gdpr_3'].append({
                    'status': 'VIOLATION' if len(missing_rights) >= 3 else 'RISK',
                    'message': f'Articles 15-21: {len(missing_rights)} data subject rights not clearly documented',
                    'found_rights': found_rights,
                    'missing_rights': missing_rights,
                    'score_deduction': score_deduction,
                    'recommendation': f'Add missing rights documentation: {", ".join(missing_rights)}'
                })
                severity = 'VIOLATION' if len(missing_rights) >= 3 else 'RISK'
                print(f"\n[{severity}] Articles 15-21: Data Subject Rights Bundle - INCOMPLETE")
                print(f"  ✓ Found ({len(found_rights)}/6): {', '.join(found_rights)}")
                print(f"  ✗ Missing ({len(missing_rights)}/6): {', '.join(missing_rights)}")
                print(f"  └─ Score Deduction: {score_deduction} points ({len(missing_rights)} × -5)")
            else:
                self.audit_report['gdpr_3'].append({
                    'status': 'PASS',
                    'message': 'Articles 15-21: All 6 data subject rights clearly documented',
                    'found_rights': found_rights
                })
                print(f"\n[PASS] Articles 15-21: Data Subject Rights Bundle - COMPLETE ✓")
                print(f"  All 6 rights documented: {', '.join(found_rights)}")
                
        except Exception as e:
            logger.error(f"Error in GDPR Pillar 3: {str(e)}")
            self.audit_report['gdpr_3'].append({
                'status': 'ERROR',
                'message': f'Rights audit failed: {str(e)}'
            })

    def _check_gdpr_pillar_4_transparency(self) -> None:
        """
        GDPR Pillar 4: Transparency & Complaints (Article 77)
        
        Requirement: Individuals must be able to lodge complaints with 
        a Supervisory Authority (e.g., ICO in UK, CNIL in France)
        
        Check: Look for keywords: "Supervisory Authority", "Lodge a complaint", "ICO", "CNIL"
               If missing: VIOLATION (-20 points)
        """
        logger.info("=== GDPR PILLAR 4: TRANSPARENCY & COMPLAINTS (Article 77) ===")
        
        if not self.privacy_policy_url:
            logger.warning("No Privacy Policy URL available")
            self.audit_report['gdpr_4'].append({
                'status': 'SKIP',
                'message': 'Article 77: Skipped - Privacy Policy not accessible'
            })
            print(f"\n[SKIP] Article 77: Privacy Policy not accessible - cannot verify complaint procedures")
            return
        
        try:
            # Get policy text
            policy_text = self._get_policy_text()
            
            if not policy_text:
                self.audit_report['gdpr_4'].append({
                    'status': 'ERROR',
                    'message': 'Article 77: Could not fetch Privacy Policy for analysis'
                })
                logger.error("Could not fetch privacy policy text")
                return
            
            # Search for complaint/authority keywords
            complaint_keywords = ['supervisory authority', 'lodge a complaint', 'ico', 'cnil', 
                                 'data protection authority', 'complaint', 'authorities',
                                 'gdpr', 'regulation']
            
            found_keywords = []
            for keyword in complaint_keywords:
                if keyword in policy_text:
                    found_keywords.append(keyword)
                    logger.info(f"Found complaint reference: {keyword}")
            
            if found_keywords:
                self.audit_report['gdpr_4'].append({
                    'status': 'PASS',
                    'message': 'Article 77: Complaints procedure with Supervisory Authority documented',
                    'keywords': found_keywords
                })
                print(f"\n[PASS] Article 77: Transparency & Complaints - DOCUMENTED")
                print(f"  ✓ Found references to: {', '.join(set(found_keywords))}")
            else:
                self.audit_report['gdpr_4'].append({
                    'status': 'VIOLATION',
                    'message': 'Article 77: No reference to complaint procedures or Supervisory Authority',
                    'score_deduction': -20,
                    'recommendation': 'Include information about complaint rights and relevant authority contact'
                })
                print(f"\n[VIOLATION] Article 77: Transparency & Complaints - MISSING (-20 points)")
                print(f"  └─ Must document: Right to lodge complaint with Supervisory Authority")
                
        except Exception as e:
            logger.error(f"Error in GDPR Pillar 4: {str(e)}")
            self.audit_report['gdpr_4'].append({
                'status': 'ERROR',
                'message': f'Complaints audit failed: {str(e)}'
            })

    def _check_gdpr_pillar_5_transfers(self) -> None:
        """
        GDPR Pillar 5: International Transfers (Articles 44-46)
        
        Requirement: When transferring personal data outside EU/EEA, 
        organizations must use approved safeguards.
        
        Check:
        1. Does policy mention "Transfer" AND "Outside EU/EEA"?
        2. If yes, check for safeguards: "Standard Contractual Clauses", "SCCs", "Adequacy Decision"
        3. If safeguards missing: RISK
        """
        logger.info("=== GDPR PILLAR 5: INTERNATIONAL TRANSFERS (Articles 44-46) ===")
        
        if not self.privacy_policy_url:
            logger.warning("No Privacy Policy URL available")
            self.audit_report['gdpr_5'].append({
                'status': 'SKIP',
                'message': 'Articles 44-46: Skipped - Privacy Policy not accessible'
            })
            print(f"\n[SKIP] Articles 44-46: Privacy Policy not accessible - cannot verify transfer safeguards")
            return
        
        try:
            # Get policy text
            policy_text = self._get_policy_text()
            
            if not policy_text:
                self.audit_report['gdpr_5'].append({
                    'status': 'ERROR',
                    'message': 'Articles 44-46: Could not fetch Privacy Policy for analysis'
                })
                logger.error("Could not fetch privacy policy text")
                return
            
            # Check for international transfer indicators
            transfer_keywords = ['transfer', 'transfer outside', 'international', 'outside eu', 'outside eea', 
                                'third country', 'outside europe']
            
            # Check for transfer safeguards
            safeguard_keywords = ['standard contractual clause', 'scc', 'adequacy decision', 
                                 'binding corporate rule', 'bcr', 'approved mechanism',
                                 'model clause', 'standard clause']
            
            # Check if there are transfers mentioned
            mentions_transfer = any(keyword in policy_text for keyword in transfer_keywords)
            
            # Check if safeguards are mentioned
            has_safeguards = any(keyword in policy_text for keyword in safeguard_keywords)
            
            found_safeguards = [kw for kw in safeguard_keywords if kw in policy_text]
            
            if not mentions_transfer:
                # No international transfers mentioned - likely only processes EU data
                self.audit_report['gdpr_5'].append({
                    'status': 'PASS',
                    'message': 'Articles 44-46: No international transfers indicated (or local processing only)'
                })
                print(f"\n[PASS] Articles 44-46: International Transfers - N/A or EU-only processing")
                
            elif mentions_transfer and has_safeguards:
                # Transfers with safeguards in place
                self.audit_report['gdpr_5'].append({
                    'status': 'PASS',
                    'message': 'Articles 44-46: International transfers with documented safeguards',
                    'safeguards': found_safeguards
                })
                print(f"\n[PASS] Articles 44-46: International Transfers - COMPLIANT with safeguards")
                print(f"  ✓ Safeguards found: {', '.join(set(found_safeguards))}")
                
            else:
                # Transfers mentioned but no safeguards documented
                self.audit_report['gdpr_5'].append({
                    'status': 'RISK',
                    'message': 'Articles 44-46: International transfers mentioned but safeguards not documented',
                    'score_deduction': -15,
                    'recommendation': 'Document transfer mechanisms (SCCs, Adequacy Decision, BCRs)'
                })
                print(f"\n[RISK] Articles 44-46: International Transfers - SAFEGUARDS MISSING (-15 points)")
                print(f"  └─ Transfers detected but no safeguards documented")
                print(f"  └─ Required: Standard Contractual Clauses, Adequacy Decision, or Binding Corporate Rules")
                
        except Exception as e:
            logger.error(f"Error in GDPR Pillar 5: {str(e)}")
            self.audit_report['gdpr_5'].append({
                'status': 'ERROR',
                'message': f'Transfer audit failed: {str(e)}'
            })

    def _generate_report(self) -> None:
        """Generate and print final audit report"""
        print("\n" + "="*70)
        print("AUDIT SUMMARY")
        print("="*70)
        
        total_modules = 7
        status_count = {'PASS': 0, 'RISK': 0, 'VIOLATION': 0, 'ERROR': 0, 'SKIP': 0}
        
        for module_key, findings in self.audit_report.items():
            module_num = module_key.split('_')[1]
            print(f"\nModule {module_num}:")
            
            for finding in findings:
                status = finding.get('status', 'UNKNOWN')
                message = finding.get('message', 'No details')
                
                if status in status_count:
                    status_count[status] += 1
                
                print(f"  [{status}] {message}")
        
        # Print final summary
        print("\n" + "-"*70)
        print("OVERALL COMPLIANCE SCORE:")
        print("-"*70)
        
        violations = status_count['VIOLATION']
        risks = status_count['RISK']
        passes = status_count['PASS']
        
        if violations == 0 and risks == 0:
            compliance_level = "HIGH ✓"
        elif violations == 0:
            compliance_level = "MEDIUM ⚠"
        else:
            compliance_level = "LOW ✗"
        
        print(f"Compliance Level: {compliance_level}")
        print(f"Violations: {violations}")
        print(f"Risks: {risks}")
        print(f"Passed: {passes}")
        print("="*70 + "\n")

    def _generate_pdf_report(self) -> str:
        """
        Generate a PDF report of the audit findings
        
        Returns:
            Path to generated PDF file
        """
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.lib import colors
        
        try:
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            pdf_filename = f"DPDP_Audit_Report_{timestamp}.pdf"
            
            # Create PDF document
            doc = SimpleDocTemplate(pdf_filename, pagesize=A4,
                                  rightMargin=0.5*inch, leftMargin=0.5*inch,
                                  topMargin=0.75*inch, bottomMargin=0.75*inch)
            
            # Container for PDF elements
            elements = []
            
            # Styles
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=20,
                textColor=colors.HexColor('#0052CC'),
                spaceAfter=12,
                alignment=1  # Center
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=14,
                textColor=colors.HexColor('#0052CC'),
                spaceAfter=10,
                spaceBefore=12
            )
            
            # Title
            title = Paragraph("DPDP ACT 2025 COMPLIANCE AUDIT REPORT", title_style)
            elements.append(title)
            
            # Audit metadata
            metadata = f"<b>Target URL:</b> {self.url}<br/><b>Audit Date:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            elements.append(Paragraph(metadata, styles['Normal']))
            elements.append(Spacer(1, 0.3*inch))
            
            # Module Results
            for module_key, findings in self.audit_report.items():
                module_num = module_key.split('_')[1]
                module_title = f"Module {module_num}"
                elements.append(Paragraph(module_title, heading_style))
                
                if findings:
                    for finding in findings:
                        status = finding.get('status', 'UNKNOWN')
                        message = finding.get('message', '')
                        
                        # Color code based on status
                        if status == 'PASS':
                            color = colors.HexColor('#28A745')
                        elif status == 'VIOLATION':
                            color = colors.HexColor('#DC3545')
                        elif status == 'RISK':
                            color = colors.HexColor('#FFC107')
                        elif status == 'SKIP':
                            color = colors.HexColor('#6C757D')
                        else:
                            color = colors.HexColor('#DC3545')
                        
                        finding_text = f"<b><font color='{color.hexval()}'>[{status}]</font></b> {message}"
                        elements.append(Paragraph(finding_text, styles['Normal']))
                        
                        # Add keywords if available
                        if 'keywords' in finding and finding['keywords']:
                            keywords = ', '.join(finding['keywords'])
                            elements.append(Paragraph(f"<i>Keywords found: {keywords}</i>", styles['Italic']))
                        
                        elements.append(Spacer(1, 0.1*inch))
                else:
                    elements.append(Paragraph("<i>No findings</i>", styles['Italic']))
                
                elements.append(Spacer(1, 0.15*inch))
            
            # Summary Statistics
            elements.append(Spacer(1, 0.2*inch))
            elements.append(Paragraph("COMPLIANCE SUMMARY", heading_style))
            
            status_count = {'PASS': 0, 'RISK': 0, 'VIOLATION': 0, 'ERROR': 0, 'SKIP': 0}
            for module_findings in self.audit_report.values():
                for finding in module_findings:
                    status = finding.get('status', 'UNKNOWN')
                    if status in status_count:
                        status_count[status] += 1
            
            violations = status_count['VIOLATION']
            risks = status_count['RISK']
            passes = status_count['PASS']
            
            if violations == 0 and risks == 0:
                compliance_level = "HIGH ✓"
            elif violations == 0:
                compliance_level = "MEDIUM ⚠"
            else:
                compliance_level = "LOW ✗"
            
            summary_data = [
                ['Metric', 'Count'],
                ['Compliance Level', compliance_level],
                ['Passed', str(passes)],
                ['Risks', str(risks)],
                ['Violations', str(violations)],
                ['Total Checks', str(passes + risks + violations)]
            ]
            
            summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0052CC')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(summary_table)
            elements.append(Spacer(1, 0.3*inch))
            
            # Footer
            footer_text = "This report was generated by the DPDP Act 2025 Compliance Auditor.<br/>For more information, visit your Privacy Policy."
            elements.append(Paragraph(footer_text, styles['Italic']))
            
            # Build PDF
            doc.build(elements)
            
            logger.info(f"PDF report generated: {pdf_filename}")
            return pdf_filename
            
        except Exception as e:
            logger.error(f"Error generating PDF report: {str(e)}")
            print(f"[WARNING] Could not generate PDF: {str(e)}")
            return None


def main():
    """Main execution block"""
    print("\n" + "="*70)
    print("COMPLIANCE AUDITOR - Multi-Law Support")
    print("A tool to audit websites for Data Protection compliance")
    print("="*70)
    
    # Get URL from user
    url = input("\nEnter the target URL to audit (e.g., example.com): ").strip()
    
    if not url:
        print("[ERROR] URL cannot be empty")
        return
    
    # Get law selection from user
    print("\nSelect which law to audit against:")
    print("1. DPDP Act 2025 (India)")
    print("2. GDPR (EU - Regulation 2016/679)")
    
    law_choice = input("\nEnter your choice (1 or 2): ").strip()
    
    if law_choice == "2":
        law = "GDPR"
    else:
        law = "DPDP"
    
    print(f"\n✓ Selected: {law}")
    
    # Create auditor instance with selected law
    auditor = DPDP_Auditor(url, law=law)
    
    # Run complete audit
    auditor.run_audit()


if __name__ == "__main__":
    main()
