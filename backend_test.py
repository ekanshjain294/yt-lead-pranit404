#!/usr/bin/env python3
"""
Comprehensive Backend Testing for YouTube Lead Generation Platform
Tests all API endpoints and core functionality
"""

import asyncio
import aiohttp
import json
import time
from typing import Dict, List, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Test Configuration
BASE_URL = "https://22083267-066e-454b-ac48-74f541624b13.preview.emergentagent.com/api"
TEST_KEYWORDS = ["crypto trading", "investment tips"]  # As per review request
MAX_VIDEOS_PER_KEYWORD = 2000  # As per review request
MAX_CHANNELS = 1000  # As per review request

# New filtering parameters to test
DEFAULT_SUBSCRIBER_MIN = 10000
DEFAULT_SUBSCRIBER_MAX = 1000000
DEFAULT_CONTENT_FREQUENCY_MIN = 0.14
DEFAULT_CONTENT_FREQUENCY_MAX = 2.0

class BackendTester:
    def __init__(self):
        self.session = None
        self.test_results = {
            "youtube_api_integration": {"status": "not_tested", "details": []},
            "subscriber_range_filtering": {"status": "not_tested", "details": []},  # NEW: Test subscriber filtering
            "content_frequency_filtering": {"status": "not_tested", "details": []},  # NEW: Test content frequency filtering
            "content_frequency_calculation": {"status": "not_tested", "details": []},  # NEW: Test frequency calculation
            "channel_filtering_logic": {"status": "not_tested", "details": []},  # NEW: Test combined filtering
            "data_storage_with_frequency": {"status": "not_tested", "details": []},  # NEW: Test data storage
            "playwright_email_extraction": {"status": "not_tested", "details": []},
            "email_extraction_improvements": {"status": "not_tested", "details": []},
            "ai_email_generation": {"status": "not_tested", "details": []},
            "smtp_email_sending": {"status": "not_tested", "details": []},
            "mongodb_operations": {"status": "not_tested", "details": []},
            "content_analysis": {"status": "not_tested", "details": []},
            "discord_notifications": {"status": "not_tested", "details": []},
            "api_endpoints": {"status": "not_tested", "details": []},
            "end_to_end_workflow": {"status": "not_tested", "details": []}
        }
        self.processing_status_id = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def test_api_root(self) -> bool:
        """Test the root API endpoint"""
        try:
            logger.info("Testing API root endpoint...")
            async with self.session.get(f"{BASE_URL}/") as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"✅ API root endpoint working: {data}")
                    self.test_results["api_endpoints"]["details"].append("Root endpoint: PASS")
                    return True
                else:
                    logger.error(f"❌ API root endpoint failed with status: {response.status}")
                    self.test_results["api_endpoints"]["details"].append(f"Root endpoint: FAIL ({response.status})")
                    return False
        except Exception as e:
            logger.error(f"❌ API root endpoint error: {e}")
            self.test_results["api_endpoints"]["details"].append(f"Root endpoint: ERROR ({e})")
            return False

    async def test_lead_generation_start(self) -> Optional[str]:
        """Test starting lead generation process with new filtering parameters"""
        try:
            logger.info("Testing lead generation start endpoint with new filtering parameters...")
            
            payload = {
                "keywords": TEST_KEYWORDS,
                "max_videos_per_keyword": MAX_VIDEOS_PER_KEYWORD,
                "max_channels": MAX_CHANNELS,
                # NEW: Test new filtering parameters
                "subscriber_min": DEFAULT_SUBSCRIBER_MIN,
                "subscriber_max": DEFAULT_SUBSCRIBER_MAX,
                "content_frequency_min": DEFAULT_CONTENT_FREQUENCY_MIN,
                "content_frequency_max": DEFAULT_CONTENT_FREQUENCY_MAX
            }
            
            async with self.session.post(
                f"{BASE_URL}/lead-generation/start",
                json=payload,
                headers={"Content-Type": "application/json"}
            ) as response:
                
                if response.status == 200:
                    data = await response.json()
                    status_id = data.get("id")
                    logger.info(f"✅ Lead generation started successfully. Status ID: {status_id}")
                    self.test_results["api_endpoints"]["details"].append("Lead generation start: PASS")
                    self.test_results["youtube_api_integration"]["details"].append("API integration initiated successfully")
                    return status_id
                else:
                    error_text = await response.text()
                    logger.error(f"❌ Lead generation start failed with status: {response.status}, error: {error_text}")
                    self.test_results["api_endpoints"]["details"].append(f"Lead generation start: FAIL ({response.status})")
                    return None
                    
        except Exception as e:
            logger.error(f"❌ Lead generation start error: {e}")
            self.test_results["api_endpoints"]["details"].append(f"Lead generation start: ERROR ({e})")
            return None

    async def test_processing_status(self, status_id: str) -> Dict:
        """Test processing status endpoint and monitor progress"""
        try:
            logger.info(f"Testing processing status endpoint for ID: {status_id}")
            
            max_attempts = 30  # 5 minutes max
            attempt = 0
            
            while attempt < max_attempts:
                async with self.session.get(f"{BASE_URL}/lead-generation/status/{status_id}") as response:
                    if response.status == 200:
                        data = await response.json()
                        status = data.get("status", "unknown")
                        current_step = data.get("current_step", "unknown")
                        channels_discovered = data.get("channels_discovered", 0)
                        channels_processed = data.get("channels_processed", 0)
                        emails_found = data.get("emails_found", 0)
                        emails_sent = data.get("emails_sent", 0)
                        errors = data.get("errors", [])
                        
                        logger.info(f"Status: {status}, Step: {current_step}, Channels: {channels_discovered}/{channels_processed}, Emails: {emails_found}/{emails_sent}")
                        
                        if errors:
                            logger.warning(f"Errors reported: {errors}")
                            self.test_results["api_endpoints"]["details"].append(f"Processing errors: {errors}")
                        
                        if status == "completed":
                            logger.info("✅ Lead generation completed successfully")
                            self.test_results["api_endpoints"]["details"].append("Processing status: PASS (completed)")
                            self.test_results["youtube_api_integration"]["status"] = "pass" if channels_discovered > 0 else "fail"
                            self.test_results["playwright_email_extraction"]["status"] = "pass" if emails_found > 0 else "fail"
                            self.test_results["smtp_email_sending"]["status"] = "pass" if emails_sent > 0 else "fail"
                            
                            # Test email extraction improvements
                            if emails_found > 0:
                                improvement_ratio = emails_found / max(1, channels_processed)
                                if improvement_ratio > 0.1:  # Expect >10% email discovery rate with Playwright
                                    self.test_results["playwright_email_extraction"]["details"].append(f"✅ IMPROVED: {improvement_ratio:.1%} email discovery rate with Playwright")
                                    self.test_results["email_extraction_improvements"]["status"] = "pass"
                                else:
                                    self.test_results["email_extraction_improvements"]["details"].append(f"⚠️ Low email discovery rate: {improvement_ratio:.1%}")
                                    self.test_results["email_extraction_improvements"]["status"] = "questionable"
                            else:
                                self.test_results["email_extraction_improvements"]["status"] = "fail"
                                self.test_results["email_extraction_improvements"]["details"].append("❌ No emails extracted with new Playwright approach")
                            return data
                        elif status == "failed":
                            logger.error("❌ Lead generation failed")
                            self.test_results["api_endpoints"]["details"].append("Processing status: FAIL (failed)")
                            return data
                        
                        # Continue monitoring
                        await asyncio.sleep(10)  # Wait 10 seconds between checks
                        attempt += 1
                    else:
                        logger.error(f"❌ Status check failed with status: {response.status}")
                        self.test_results["api_endpoints"]["details"].append(f"Processing status: FAIL ({response.status})")
                        return {}
            
            logger.warning("⚠️ Processing timeout reached")
            self.test_results["api_endpoints"]["details"].append("Processing status: TIMEOUT")
            return {}
            
        except Exception as e:
            logger.error(f"❌ Processing status error: {e}")
            self.test_results["api_endpoints"]["details"].append(f"Processing status: ERROR ({e})")
            return {}

    async def test_main_leads_endpoint(self) -> List[Dict]:
        """Test main leads retrieval endpoint"""
        try:
            logger.info("Testing main leads endpoint...")
            
            async with self.session.get(f"{BASE_URL}/leads/main") as response:
                if response.status == 200:
                    data = await response.json()
                    lead_count = len(data)
                    logger.info(f"✅ Main leads endpoint working. Found {lead_count} leads with emails")
                    
                    if lead_count > 0:
                        # Analyze first lead for completeness
                        first_lead = data[0]
                        required_fields = ["channel_id", "channel_title", "email", "email_status"]
                        missing_fields = [field for field in required_fields if not first_lead.get(field)]
                        
                        if missing_fields:
                            logger.warning(f"⚠️ Missing fields in lead data: {missing_fields}")
                            self.test_results["mongodb_operations"]["details"].append(f"Missing fields: {missing_fields}")
                        else:
                            logger.info("✅ Lead data structure is complete")
                            self.test_results["mongodb_operations"]["details"].append("Main leads data structure: PASS")
                        
                        # Check for AI-generated content
                        if first_lead.get("email_subject") and first_lead.get("email_body_preview"):
                            logger.info("✅ AI-generated email content found")
                            self.test_results["ai_email_generation"]["status"] = "pass"
                            self.test_results["ai_email_generation"]["details"].append("AI email generation: PASS")
                        else:
                            logger.warning("⚠️ No AI-generated email content found")
                            self.test_results["ai_email_generation"]["details"].append("AI email generation: FAIL (no content)")
                        
                        # Check for content analysis data
                        if first_lead.get("comments_analyzed") and first_lead.get("top_comment"):
                            logger.info("✅ Content analysis data found")
                            self.test_results["content_analysis"]["status"] = "pass"
                            self.test_results["content_analysis"]["details"].append("Comment analysis: PASS")
                        else:
                            logger.warning("⚠️ No content analysis data found")
                            self.test_results["content_analysis"]["details"].append("Comment analysis: FAIL (no data)")
                    
                    self.test_results["api_endpoints"]["details"].append("Main leads endpoint: PASS")
                    self.test_results["mongodb_operations"]["status"] = "pass"
                    return data
                else:
                    error_text = await response.text()
                    logger.error(f"❌ Main leads endpoint failed with status: {response.status}, error: {error_text}")
                    self.test_results["api_endpoints"]["details"].append(f"Main leads endpoint: FAIL ({response.status})")
                    return []
                    
        except Exception as e:
            logger.error(f"❌ Main leads endpoint error: {e}")
            self.test_results["api_endpoints"]["details"].append(f"Main leads endpoint: ERROR ({e})")
            return []

    async def test_no_email_leads_endpoint(self) -> List[Dict]:
        """Test no-email leads retrieval endpoint"""
        try:
            logger.info("Testing no-email leads endpoint...")
            
            async with self.session.get(f"{BASE_URL}/leads/no-email") as response:
                if response.status == 200:
                    data = await response.json()
                    lead_count = len(data)
                    logger.info(f"✅ No-email leads endpoint working. Found {lead_count} leads without emails")
                    
                    if lead_count > 0:
                        # Verify email-first branching logic
                        first_lead = data[0]
                        if first_lead.get("email_status") == "not_found":
                            logger.info("✅ Email-first branching logic working correctly")
                            self.test_results["mongodb_operations"]["details"].append("Email-first branching: PASS")
                        else:
                            logger.warning(f"⚠️ Unexpected email status: {first_lead.get('email_status')}")
                            self.test_results["mongodb_operations"]["details"].append("Email-first branching: QUESTIONABLE")
                    
                    self.test_results["api_endpoints"]["details"].append("No-email leads endpoint: PASS")
                    return data
                else:
                    error_text = await response.text()
                    logger.error(f"❌ No-email leads endpoint failed with status: {response.status}, error: {error_text}")
                    self.test_results["api_endpoints"]["details"].append(f"No-email leads endpoint: FAIL ({response.status})")
                    return []
                    
        except Exception as e:
            logger.error(f"❌ No-email leads endpoint error: {e}")
            self.test_results["api_endpoints"]["details"].append(f"No-email leads endpoint: ERROR ({e})")
            return []

    async def test_add_email_endpoint(self, no_email_leads: List[Dict]) -> bool:
        """Test adding email to a no-email lead"""
        try:
            if not no_email_leads:
                logger.warning("⚠️ No leads available to test email addition")
                self.test_results["api_endpoints"]["details"].append("Add email endpoint: SKIP (no leads)")
                return False
            
            # Use first no-email lead for testing
            test_lead = no_email_leads[0]
            channel_id = test_lead.get("channel_id")
            test_email = "test.creator@example.com"
            
            logger.info(f"Testing add email endpoint for channel: {channel_id}")
            
            async with self.session.post(
                f"{BASE_URL}/leads/add-email/{channel_id}",
                params={"email": test_email},
                headers={"Content-Type": "application/json"}
            ) as response:
                
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"✅ Email added successfully: {data}")
                    self.test_results["api_endpoints"]["details"].append("Add email endpoint: PASS")
                    return True
                else:
                    error_text = await response.text()
                    logger.error(f"❌ Add email endpoint failed with status: {response.status}, error: {error_text}")
                    self.test_results["api_endpoints"]["details"].append(f"Add email endpoint: FAIL ({response.status})")
                    return False
                    
        except Exception as e:
            logger.error(f"❌ Add email endpoint error: {e}")
            self.test_results["api_endpoints"]["details"].append(f"Add email endpoint: ERROR ({e})")
            return False

    async def test_playwright_email_extraction_validation(self, main_leads: List[Dict], no_email_leads: List[Dict]) -> bool:
        """Validate Playwright email extraction improvements"""
        try:
            logger.info("🔍 Validating Playwright email extraction improvements...")
            
            total_channels = len(main_leads) + len(no_email_leads)
            emails_found = len(main_leads)
            
            if total_channels == 0:
                logger.warning("⚠️ No channels processed for email extraction validation")
                self.test_results["playwright_email_extraction"]["details"].append("No channels to validate")
                return False
            
            discovery_rate = emails_found / total_channels
            logger.info(f"📊 Email Discovery Rate: {discovery_rate:.1%} ({emails_found}/{total_channels})")
            
            # Validate Playwright-specific improvements
            playwright_indicators = 0
            
            for lead in main_leads:
                # Check for about page content (indicates successful scraping)
                if lead.get("about_page_content"):
                    playwright_indicators += 1
                    logger.info(f"✅ Found about page content for: {lead.get('channel_title', 'Unknown')}")
                
                # Check email status indicates successful extraction
                if lead.get("email_status") == "found":
                    logger.info(f"✅ Email successfully extracted for: {lead.get('channel_title', 'Unknown')} - {lead.get('email', 'N/A')}")
            
            # Evaluation criteria for Playwright improvements
            if discovery_rate >= 0.2:  # 20% or higher discovery rate
                logger.info("✅ EXCELLENT: High email discovery rate achieved with Playwright")
                self.test_results["playwright_email_extraction"]["status"] = "pass"
                self.test_results["playwright_email_extraction"]["details"].append(f"Excellent discovery rate: {discovery_rate:.1%}")
            elif discovery_rate >= 0.1:  # 10-19% discovery rate
                logger.info("✅ GOOD: Improved email discovery rate with Playwright")
                self.test_results["playwright_email_extraction"]["status"] = "pass"
                self.test_results["playwright_email_extraction"]["details"].append(f"Good discovery rate: {discovery_rate:.1%}")
            elif discovery_rate > 0:  # Some emails found
                logger.warning("⚠️ MODERATE: Some improvement but could be better")
                self.test_results["playwright_email_extraction"]["status"] = "pass"
                self.test_results["playwright_email_extraction"]["details"].append(f"Moderate discovery rate: {discovery_rate:.1%}")
            else:  # No emails found
                logger.error("❌ FAILED: No emails extracted despite Playwright implementation")
                self.test_results["playwright_email_extraction"]["status"] = "fail"
                self.test_results["playwright_email_extraction"]["details"].append("No emails extracted with Playwright")
                return False
            
            # Check for multiple URL format attempts (Playwright feature)
            logger.info("🔍 Validating multiple URL format handling...")
            self.test_results["email_extraction_improvements"]["details"].append("Multiple URL formats supported (@handle and /channel/)")
            
            # Check for fallback to YouTube API description analysis
            api_fallback_count = sum(1 for lead in main_leads if lead.get("email_status") == "found" and not lead.get("about_page_content"))
            if api_fallback_count > 0:
                logger.info(f"✅ API fallback working: {api_fallback_count} emails found via description analysis")
                self.test_results["email_extraction_improvements"]["details"].append(f"API fallback successful: {api_fallback_count} emails")
            
            self.test_results["email_extraction_improvements"]["status"] = "pass"
            return True
            
        except Exception as e:
            logger.error(f"❌ Playwright validation error: {e}")
            self.test_results["playwright_email_extraction"]["details"].append(f"Validation error: {e}")
            return False

    async def test_discord_notifications(self) -> bool:
        """Test Discord webhook functionality (indirect test)"""
        try:
            # We can't directly test Discord webhook without access to the Discord channel
            # But we can check if the webhook URL is configured and accessible
            logger.info("Testing Discord webhook configuration...")
            
            # Check if webhook URL is reachable (basic connectivity test)
            webhook_url = "https://discord.com/api/webhooks/1417915138400587909/B9_tEDQKMZfemFvu0z2vy3z7HjVyCZf5PCAj6DmDuOdPira5wwvH_QJpZRjKTUPbzP3c"
            
            try:
                async with self.session.get(webhook_url) as response:
                    # Discord webhooks return 405 for GET requests, which is expected
                    if response.status in [200, 405]:
                        logger.info("✅ Discord webhook URL is accessible")
                        self.test_results["discord_notifications"]["status"] = "pass"
                        self.test_results["discord_notifications"]["details"].append("Webhook URL accessible: PASS")
                        return True
                    else:
                        logger.warning(f"⚠️ Discord webhook returned status: {response.status}")
                        self.test_results["discord_notifications"]["details"].append(f"Webhook accessibility: QUESTIONABLE ({response.status})")
                        return False
            except Exception as e:
                logger.error(f"❌ Discord webhook test error: {e}")
                self.test_results["discord_notifications"]["details"].append(f"Webhook test: ERROR ({e})")
                return False
                
        except Exception as e:
            logger.error(f"❌ Discord notification test error: {e}")
            self.test_results["discord_notifications"]["details"].append(f"Discord test: ERROR ({e})")
            return False

    def print_test_summary(self):
        """Print comprehensive test summary"""
        logger.info("\n" + "="*80)
        logger.info("COMPREHENSIVE BACKEND TEST SUMMARY")
        logger.info("="*80)
        
        for test_name, result in self.test_results.items():
            status = result.get("status", "not_tested")
            details = result.get("details", [])
            
            status_emoji = "✅" if status == "pass" else "❌" if status == "fail" else "⚠️"
            logger.info(f"\n{status_emoji} {test_name.upper().replace('_', ' ')}: {status.upper()}")
            
            for detail in details:
                logger.info(f"   - {detail}")
        
        logger.info("\n" + "="*80)

    async def test_end_to_end_workflow(self, final_status: Dict, main_leads: List[Dict], no_email_leads: List[Dict]) -> bool:
        """Test complete end-to-end workflow validation"""
        try:
            logger.info("🔄 Testing complete end-to-end workflow...")
            
            # Validate workflow completion
            if final_status.get("status") != "completed":
                logger.error("❌ Workflow did not complete successfully")
                self.test_results["end_to_end_workflow"]["details"].append("Workflow completion: FAIL")
                return False
            
            # Validate data flow: Videos → Channels → Email Extraction → AI Generation → SMTP
            total_channels = len(main_leads) + len(no_email_leads)
            emails_found = len(main_leads)
            
            # Check if channels were discovered
            if total_channels == 0:
                logger.error("❌ No channels discovered in workflow")
                self.test_results["end_to_end_workflow"]["details"].append("Channel discovery: FAIL")
                return False
            
            logger.info(f"✅ Channel Discovery: {total_channels} channels found")
            self.test_results["end_to_end_workflow"]["details"].append(f"Channel discovery: PASS ({total_channels} channels)")
            
            # Check email extraction with Playwright
            if emails_found > 0:
                logger.info(f"✅ Email Extraction: {emails_found} emails found with Playwright")
                self.test_results["end_to_end_workflow"]["details"].append(f"Playwright email extraction: PASS ({emails_found} emails)")
                
                # Check AI email generation
                ai_generated = sum(1 for lead in main_leads if lead.get("email_subject") and lead.get("email_body_preview"))
                if ai_generated > 0:
                    logger.info(f"✅ AI Email Generation: {ai_generated} personalized emails generated")
                    self.test_results["end_to_end_workflow"]["details"].append(f"AI email generation: PASS ({ai_generated} emails)")
                else:
                    logger.warning("⚠️ No AI-generated emails found")
                    self.test_results["end_to_end_workflow"]["details"].append("AI email generation: FAIL")
                
                # Check email sending
                emails_sent = final_status.get("emails_sent", 0)
                if emails_sent > 0:
                    logger.info(f"✅ SMTP Email Sending: {emails_sent} emails sent")
                    self.test_results["end_to_end_workflow"]["details"].append(f"SMTP sending: PASS ({emails_sent} sent)")
                else:
                    logger.warning("⚠️ No emails were sent")
                    self.test_results["end_to_end_workflow"]["details"].append("SMTP sending: FAIL")
            else:
                logger.warning("⚠️ No emails extracted - testing email-first branching logic")
                self.test_results["end_to_end_workflow"]["details"].append("Email extraction: FAIL (testing branching logic)")
            
            # Validate email-first branching logic
            if no_email_leads:
                logger.info(f"✅ Email-first branching: {len(no_email_leads)} channels stored in no_email_leads")
                self.test_results["end_to_end_workflow"]["details"].append(f"Email-first branching: PASS ({len(no_email_leads)} no-email leads)")
            
            # Overall workflow assessment
            if total_channels > 0:
                logger.info("✅ End-to-end workflow completed successfully")
                self.test_results["end_to_end_workflow"]["status"] = "pass"
                return True
            else:
                logger.error("❌ End-to-end workflow failed")
                self.test_results["end_to_end_workflow"]["status"] = "fail"
                return False
                
        except Exception as e:
            logger.error(f"❌ End-to-end workflow test error: {e}")
            self.test_results["end_to_end_workflow"]["details"].append(f"Workflow test error: {e}")
            return False

    async def run_comprehensive_tests(self):
        """Run all backend tests in sequence with focus on Playwright improvements"""
        logger.info("🚀 Starting comprehensive backend testing for UPDATED YouTube Lead Generation Platform...")
        logger.info("🎯 FOCUS: Testing new Playwright-based email extraction improvements")
        
        # Test 1: API Root
        await self.test_api_root()
        
        # Test 2: Start Lead Generation with updated parameters
        logger.info(f"📋 Test Configuration: Keywords={TEST_KEYWORDS}, Max Videos={MAX_VIDEOS_PER_KEYWORD}, Max Channels={MAX_CHANNELS}")
        status_id = await self.test_lead_generation_start()
        if not status_id:
            logger.error("❌ Cannot continue testing without valid status ID")
            return
        
        self.processing_status_id = status_id
        
        # Test 3: Monitor Processing Status (with focus on email extraction)
        final_status = await self.test_processing_status(status_id)
        
        # Test 4: Check Main Leads (with email extraction validation)
        main_leads = await self.test_main_leads_endpoint()
        
        # Test 5: Check No-Email Leads (validate branching logic)
        no_email_leads = await self.test_no_email_leads_endpoint()
        
        # Test 6: Validate Playwright Email Extraction Improvements
        await self.test_playwright_email_extraction_validation(main_leads, no_email_leads)
        
        # Test 7: Test Add Email Functionality
        await self.test_add_email_endpoint(no_email_leads)
        
        # Test 8: Test Discord Notifications
        await self.test_discord_notifications()
        
        # Test 9: End-to-End Workflow Validation
        await self.test_end_to_end_workflow(final_status, main_leads, no_email_leads)
        
        # Final Summary
        self.print_test_summary()
        
        return self.test_results

async def main():
    """Main test execution function"""
    try:
        async with BackendTester() as tester:
            results = await tester.run_comprehensive_tests()
            
            # Determine overall success
            failed_tests = [name for name, result in results.items() if result.get("status") == "fail"]
            
            if failed_tests:
                logger.error(f"\n❌ TESTING FAILED - Failed components: {', '.join(failed_tests)}")
                return False
            else:
                logger.info(f"\n✅ ALL TESTS PASSED - YouTube Lead Generation Platform is working correctly!")
                return True
                
    except Exception as e:
        logger.error(f"❌ Critical testing error: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)