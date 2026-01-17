"""
Input validation utilities for Streamlit web forms
"""

import re
from urllib.parse import urlparse
import streamlit as st


class URLValidator:
    """Validator for website URLs"""
    
    @staticmethod
    def validate_url(url: str) -> tuple[bool, str]:
        """
        Validate and normalize a URL
        
        Args:
            url: URL string to validate
            
        Returns:
            Tuple of (is_valid, message_or_normalized_url)
        """
        if not url:
            return False, "URL cannot be empty"
        
        url = url.strip()
        
        # Add https:// if no protocol
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Basic URL pattern check
        url_pattern = r'^https?://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}(/[^\s]*)?$'
        if not re.match(url_pattern, url):
            return False, "Invalid URL format. Examples: example.com or https://example.com/path"
        
        # Check for common mistakes
        if ' ' in url:
            return False, "URL cannot contain spaces"
        
        if '..' in url:
            return False, "Invalid URL path"
        
        try:
            parsed = urlparse(url)
            if not parsed.netloc:
                return False, "Invalid URL: missing domain"
            
            # Check domain has at least one dot
            if '.' not in parsed.netloc:
                return False, "Invalid domain: must be in format 'example.com'"
            
        except Exception as e:
            return False, f"URL parsing error: {str(e)}"
        
        return True, url
    
    @staticmethod
    def is_valid_policy_url(url: str) -> bool:
        """Quick check for policy URL (optional, can be lenient)"""
        if not url:
            return True  # Optional field
        
        is_valid, _ = URLValidator.validate_url(url)
        return is_valid


class InputValidator:
    """General input validation"""
    
    @staticmethod
    def validate_audit_inputs(url: str, regulation: str) -> tuple[bool, str]:
        """
        Validate audit form inputs
        
        Args:
            url: Website URL
            regulation: Selected regulation
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Validate URL
        is_valid, message = URLValidator.validate_url(url)
        if not is_valid:
            return False, message
        
        # Validate regulation
        valid_regulations = ["DPDP Act 2025 (India)", "GDPR (EU 2016/679)"]
        if regulation not in valid_regulations:
            return False, "Please select a valid regulation from the dropdown"
        
        return True, ""
    
    @staticmethod
    def show_validation_error(message: str):
        """Display validation error with styling"""
        st.error(f"❌ {message}")
    
    @staticmethod
    def show_validation_warning(message: str):
        """Display validation warning with styling"""
        st.warning(f"⚠️ {message}")
    
    @staticmethod
    def show_validation_success(message: str):
        """Display validation success with styling"""
        st.success(f"✅ {message}")


class FormValidator:
    """Comprehensive form validation"""
    
    @staticmethod
    def validate_and_prepare_audit(url_input: str, policy_url_input: str, regulation: str) -> dict:
        """
        Complete validation and preparation for audit execution
        
        Args:
            url_input: Target website URL
            policy_url_input: Privacy policy URL (optional)
            regulation: Selected regulation
            
        Returns:
            Dictionary with validation results and normalized inputs or None if invalid
        """
        result = {
            'valid': False,
            'errors': [],
            'warnings': [],
            'url': None,
            'policy_url': None,
            'regulation': None,
            'law': None
        }
        
        # Validate URL
        url_valid, url_message = URLValidator.validate_url(url_input)
        if not url_valid:
            result['errors'].append(url_message)
        else:
            result['url'] = url_message  # Normalized URL
        
        # Validate policy URL if provided
        if policy_url_input.strip():
            policy_valid, policy_message = URLValidator.validate_url(policy_url_input)
            if not policy_valid:
                result['errors'].append(f"Policy URL Error: {policy_message}")
            else:
                result['policy_url'] = policy_message  # Normalized URL
        
        # Validate regulation
        valid_regulations = ["DPDP Act 2025 (India)", "GDPR (EU 2016/679)"]
        if regulation not in valid_regulations:
            result['errors'].append("Please select a valid regulation from the dropdown")
        else:
            result['regulation'] = regulation
            # Map regulation to law code
            result['law'] = "GDPR" if "GDPR" in regulation else "DPDP"
        
        # Overall validation
        if not result['errors']:
            result['valid'] = True
        
        return result


def validate_and_show_errors(validation_result: dict) -> bool:
    """
    Display validation errors/warnings and return if valid
    
    Args:
        validation_result: Result from FormValidator.validate_and_prepare_audit()
        
    Returns:
        True if valid, False otherwise
    """
    if validation_result['errors']:
        for error in validation_result['errors']:
            InputValidator.show_validation_error(error)
        return False
    
    if validation_result['warnings']:
        for warning in validation_result['warnings']:
            InputValidator.show_validation_warning(warning)
    
    return True
