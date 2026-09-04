from django.test import TestCase
from django.urls import reverse

class EInvoiceViewsTestCase(TestCase):
    def test_home_page(self):
        response = self.client.get(reverse('invoices:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'invoices/home.html')

    def test_about_page(self):
        response = self.client.get(reverse('invoices:about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'invoices/about.html')

    def test_features_page(self):
        response = self.client.get(reverse('invoices:features'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'invoices/features.html')

    def test_verify_invoice_page(self):
        response = self.client.get(reverse('invoices:verify_invoice'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'invoices/verify_invoice.html')

    def test_contact_page_get_and_post(self):
        response = self.client.get(reverse('invoices:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'invoices/contact.html')

        post_data = {'name': 'John Doe', 'email': 'john@example.com', 'message': 'Test inquiry'}
        post_response = self.client.post(reverse('invoices:contact'), post_data)
        self.assertEqual(post_response.status_code, 302) # Redirects back to contact page

    def test_create_shopkeeper_redirects_unauthenticated(self):
        response = self.client.get(reverse('invoices:create_shopkeeper'))
        self.assertEqual(response.status_code, 302) # Redirects to login

