import streamlit as st
import pandas as pd
from datetime import datetime
import time
import requests
import json
import os

# Configure page
st.set_page_config(
    page_title="AI Facebook Ads Copy Generator - Vigoshop",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

class AIFacebookAdsCopyGenerator:
    def __init__(self):
        self.sample_products = [
            {
                'id': 'digicam',
                'name': 'Zunanja in notranja brezžična kamera DIGICAM',
                'price': '33.99',
                'category': 'Security & Electronics',
                'description': 'Professional wireless security camera for indoor and outdoor use',
                'key_features': 'Wireless, HD quality, indoor/outdoor, easy setup',
                'target_audience': 'homeowners, security-conscious individuals'
            },
            {
                'id': 'sixpack',
                'name': 'Trener za trebušne mišice SIXPACK',
                'price': '19.99',
                'category': 'Fitness & Health',
                'description': 'Effortless fat burning and core strengthening device',
                'key_features': 'No-effort training, fat burning, portable',
                'target_audience': 'fitness enthusiasts, busy professionals'
            },
            {
                'id': 'brenchie',
                'name': 'Akumulatorska ročna žaga BRENCHIE',
                'price': '30.99',
                'category': 'Tools & Garden',
                'description': 'Portable cordless hand saw for various cutting tasks',
                'key_features': 'Cordless, portable, powerful, versatile',
                'target_audience': 'DIY enthusiasts, gardeners, professionals'
            },
            {
                'id': 'smily',
                'name': 'Električni čistilec zob SMILY',
                'price': '19.99',
                'category': 'Health & Beauty',
                'description': 'Electric ultrasonic teeth cleaner for professional dental care',
                'key_features': 'Ultrasonic technology, professional cleaning, easy to use',
                'target_audience': 'health-conscious individuals, dental care enthusiasts'
            },
            {
                'id': 'antimosquito',
                'name': 'LED naprava proti komarjem ANTIMOSQUITO',
                'price': '14.99',
                'category': 'Home & Garden',
                'description': 'Safe and silent LED mosquito killer device',
                'key_features': 'LED technology, safe, silent, effective',
                'target_audience': 'families, outdoor enthusiasts, homeowners'
            }
        ]
        
        # Template-based copy generation (fallback)
        self.copy_templates = {
            'Problem-Solution': self._problem_solution_template,
            'Social Proof': self._social_proof_template,
            'FOMO': self._fomo_template,
            'Value-Focused': self._value_focused_template
        }
        
        self.challenges = {
            'Security & Electronics': 'home security concerns',
            'Fitness & Health': 'achieving your fitness goals',
            'Tools & Garden': 'time-consuming manual work',
            'Health & Beauty': 'expensive dental treatments',
            'Home & Garden': 'annoying mosquito problems'
        }
        
        self.benefits = {
            'Security & Electronics': 'Professional security monitoring made simple',
            'Fitness & Health': 'Effortless fitness results without gym time',
            'Tools & Garden': 'Professional results in half the time',
            'Health & Beauty': 'Professional dental cleaning at home',
            'Home & Garden': 'Peaceful, mosquito-free environment'
        }

    def get_challenge_for_product(self, product):
        return self.challenges.get(product['category'], 'everyday challenges')

    def get_main_benefit(self, product):
        return self.benefits.get(product['category'], 'Amazing results you can trust')

    def _problem_solution_template(self, product):
        return {
            'headline': f"Stop struggling with {self.get_challenge_for_product(product)}! 💪",
            'primary': f"Tired of {self.get_challenge_for_product(product)}? {product['name']} changes everything! {self.get_main_benefit(product)} for just €{product['price']}. Thousands of satisfied customers can't be wrong! ⭐⭐⭐⭐⭐",
            'cta': 'Get Yours Now - Limited Time Offer!',
            'hashtags': f"#{product['category'].replace(' ', '').replace('&', '')} #Innovation #QualityProducts #VigoshopDeals"
        }

    def _social_proof_template(self, product):
        first_word = product['name'].split(' ')[0]
        return {
            'headline': f"Why Everyone's Talking About {first_word}! 🔥",
            'primary': f"Join thousands who've discovered {product['name']}! {self.get_main_benefit(product)}. Real customers, real results. Starting at just €{product['price']} with fast EU delivery! 🚚💨",
            'cta': 'Join the Revolution - Order Today!',
            'hashtags': f"#CustomerFavorite #{product['category'].replace(' ', '').replace('&', '')} #FastDelivery #EUShipping"
        }

    def _fomo_template(self, product):
        return {
            'headline': f"⚡ FLASH SALE: {product['name']} - Don't Miss Out!",
            'primary': f"LIMITED TIME: Get {product['name']} for just €{product['price']}! {self.get_main_benefit(product)}. This deal won't last - secure yours before it's gone! ⏰",
            'cta': 'Claim Your Deal Now!',
            'hashtags': f"#FlashSale #LimitedOffer #DontMissOut #{product['category'].replace(' ', '').replace('&', '')}"
        }

    def _value_focused_template(self, product):
        return {
            'headline': "Premium Quality at Unbeatable Price! 💎",
            'primary': f"Why pay more? {product['name']} delivers {self.get_main_benefit(product)} at just €{product['price']}. Premium quality, lowest prices, fast EU shipping. Your wallet will thank you! 💰",
            'cta': 'Shop Smart - Buy Now!',
            'hashtags': "#BestPrice #PremiumQuality #SmartShopping #ValueForMoney"
        }

    def call_groq_api(self, prompt, api_key):
        """Call Groq API for AI-powered copy generation"""
        url = "https://api.groq.com/openai/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "llama-3.3-70b-versatile",  # Fast and free model
            "messages": [
                {
                    "role": "system", 
                    "content": "You are an expert Facebook ads copywriter specializing in e-commerce. Create compelling, conversion-focused ad copy that drives engagement and sales. Keep headlines under 125 characters and use emojis strategically."
                },
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 500,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            else:
                return None
        except Exception as e:
            st.error(f"AI API Error: {str(e)}")
            return None

    def generate_ai_copy(self, product, style, api_key):
        """Generate AI-powered copy for a specific style"""
        style_prompts = {
            'Problem-Solution': f"""
            Create a Facebook ad copy using the Problem-Solution approach for this product:
            
            Product: {product['name']}
            Price: €{product['price']}
            Category: {product['category']}
            Description: {product.get('description', '')}
            Key Features: {product.get('key_features', '')}
            Target Audience: {product.get('target_audience', '')}
            
            Format your response as JSON:
            {{
                "headline": "Engaging headline under 125 characters",
                "primary": "Compelling primary text that identifies a problem and presents the solution",
                "cta": "Strong call-to-action",
                "hashtags": "Relevant hashtags including #VigoshopDeals"
            }}
            """,
            
            'Social Proof': f"""
            Create a Facebook ad copy using Social Proof approach for this product:
            
            Product: {product['name']}
            Price: €{product['price']}
            Category: {product['category']}
            Description: {product.get('description', '')}
            Key Features: {product.get('key_features', '')}
            Target Audience: {product.get('target_audience', '')}
            
            Focus on customer testimonials, reviews, and popularity. Format as JSON:
            {{
                "headline": "Engaging headline under 125 characters",
                "primary": "Primary text emphasizing customer satisfaction and popularity",
                "cta": "Strong call-to-action",
                "hashtags": "Relevant hashtags including #CustomerFavorite"
            }}
            """,
            
            'FOMO': f"""
            Create a Facebook ad copy using FOMO (Fear of Missing Out) approach for this product:
            
            Product: {product['name']}
            Price: €{product['price']}
            Category: {product['category']}
            Description: {product.get('description', '')}
            Key Features: {product.get('key_features', '')}
            Target Audience: {product.get('target_audience', '')}
            
            Create urgency and scarcity. Format as JSON:
            {{
                "headline": "Urgent headline under 125 characters",
                "primary": "Primary text creating urgency and fear of missing out",
                "cta": "Urgent call-to-action",
                "hashtags": "Relevant hashtags including #LimitedOffer"
            }}
            """,
            
            'Value-Focused': f"""
            Create a Facebook ad copy using Value-Focused approach for this product:
            
            Product: {product['name']}
            Price: €{product['price']}
            Category: {product['category']}
            Description: {product.get('description', '')}
            Key Features: {product.get('key_features', '')}
            Target Audience: {product.get('target_audience', '')}
            
            Emphasize value, savings, and smart purchasing. Format as JSON:
            {{
                "headline": "Value-focused headline under 125 characters",
                "primary": "Primary text emphasizing great value and smart shopping",
                "cta": "Value-driven call-to-action",
                "hashtags": "Relevant hashtags including #BestPrice"
            }}
            """
        }
        
        prompt = style_prompts.get(style, style_prompts['Problem-Solution'])
        ai_response = self.call_groq_api(prompt, api_key)
        
        if ai_response:
            try:
                # Try to parse JSON response
                if '{' in ai_response and '}' in ai_response:
                    json_start = ai_response.find('{')
                    json_end = ai_response.rfind('}') + 1
                    json_str = ai_response[json_start:json_end]
                    copy_data = json.loads(json_str)
                    copy_data['style'] = style
                    copy_data['product'] = product['name']
                    copy_data['ai_generated'] = True
                    return copy_data
                else:
                    # If no JSON, create structured response from text
                    lines = ai_response.split('\n')
                    return {
                        'headline': f"AI Generated: {product['name']} - Special Offer! 🔥",
                        'primary': ai_response[:200] + "...",
                        'cta': 'Buy Now!',
                        'hashtags': f"#{product['category'].replace(' ', '').replace('&', '')} #AIGenerated #VigoshopDeals",
                        'style': style,
                        'product': product['name'],
                        'ai_generated': True
                    }
            except json.JSONDecodeError:
                # Fallback to template if JSON parsing fails
                return self._fallback_to_template(product, style)
        else:
            return self._fallback_to_template(product, style)

    def _fallback_to_template(self, product, style):
        """Fallback to template-based generation if AI fails"""
        template_func = self.copy_templates.get(style, self.copy_templates['Problem-Solution'])
        copy_data = template_func(product)
        copy_data['style'] = style
        copy_data['product'] = product['name']
        copy_data['ai_generated'] = False
        return copy_data

    def generate_copies(self, product, use_ai=False, api_key=None):
        """Generate all ad copy variations for a product"""
        copies = []
        styles = ['Problem-Solution', 'Social Proof', 'FOMO', 'Value-Focused']
        
        for style in styles:
            if use_ai and api_key:
                copy_data = self.generate_ai_copy(product, style, api_key)
            else:
                copy_data = self._fallback_to_template(product, style)
            copies.append(copy_data)
        
        return copies

    def export_to_txt(self, copies):
        """Export copies to text format"""
        export_text = f"Facebook Ad Copies - Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        export_text += "=" * 70 + "\n\n"
        
        for copy in copies:
            ai_indicator = " (AI Generated)" if copy.get('ai_generated', False) else " (Template Based)"
            export_text += f"Style: {copy['style']}{ai_indicator}\n"
            export_text += f"Product: {copy['product']}\n\n"
            export_text += f"Headline: {copy['headline']}\n\n"
            export_text += f"Primary Text: {copy['primary']}\n\n"
            export_text += f"CTA: {copy['cta']}\n\n"
            export_text += f"Hashtags: {copy['hashtags']}\n\n"
            export_text += "=" * 70 + "\n\n"
        
        return export_text

    def export_to_csv(self, copies):
        """Export copies to CSV format"""
        df = pd.DataFrame(copies)
        return df.to_csv(index=False)

def main():
    generator = AIFacebookAdsCopyGenerator()
    
    # Header
    st.title("🤖 AI-Powered Facebook Ads Copy Generator")
    st.subheader("Create compelling Facebook ad copy for Vigoshop products using AI")
    
    # AI Configuration in sidebar
    with st.sidebar:
        st.header("🔧 AI Configuration")
        
        use_ai = st.toggle("Enable AI Generation", value=False)
        
        if use_ai:
            st.info("🚀 Using Groq AI (Free Llama3 model)")
            api_key = st.text_input(
                "Groq API Key", 
                type="password", 
                help="Get your free API key from https://console.groq.com/"
            )
            if api_key:
                st.success("✅ API Key configured")
            else:
                st.warning("⚠️ Please enter your Groq API key to use AI generation")
        else:
            st.info("📝 Using template-based generation")
            api_key = None
        
        st.markdown("---")
        
        # Product Selection
        st.header("Product Selection")
        
        # Product type selection
        product_type = st.radio(
            "Choose product source:",
            ["Sample Vigoshop Products", "Custom Product"]
        )
        
        if product_type == "Sample Vigoshop Products":
            # Sample product dropdown
            product_names = [f"{p['name']} - €{p['price']}" for p in generator.sample_products]
            selected_product_idx = st.selectbox(
                "Select a Vigoshop product:",
                range(len(product_names)),
                format_func=lambda x: product_names[x]
            )
            selected_product = generator.sample_products[selected_product_idx]
            
        else:
            # Custom product form
            st.subheader("Custom Product Details")
            custom_product = {
                'name': st.text_input("Product Name", placeholder="Enter product name..."),
                'price': st.text_input("Price (EUR)", placeholder="29.99"),
                'category': st.selectbox(
                    "Category",
                    ["Security & Electronics", "Fitness & Health", "Tools & Garden", 
                     "Health & Beauty", "Home & Garden"]
                ),
                'description': st.text_area("Description", placeholder="Brief product description..."),
                'key_features': st.text_input("Key Features", placeholder="Feature 1, Feature 2, Feature 3..."),
                'target_audience': st.text_input("Target Audience", placeholder="young professionals, parents...")
            }
            selected_product = custom_product
        
        # Generate button
        can_generate = selected_product.get('name') and selected_product.get('price')
        if use_ai:
            can_generate = can_generate and api_key
            
        generate_button = st.button(
            "🚀 Generate AI Ad Copies" if use_ai else "🚀 Generate Ad Copies", 
            type="primary", 
            use_container_width=True,
            disabled=not can_generate
        )
    
    # Main content area
    col1, col2 = st.columns([1, 2])
    check = False
    error = ""
    try:
        float(selected_product.get('price', ''))
        check = True
    except ValueError:
        error = "Invalid price format. Please enter a numeric value."

    with col1:
        st.header("📋 Product Preview")
        if selected_product and selected_product.get('name') and check:
            st.info(f"**Product:** {selected_product['name']}")
            st.info(f"**Price:** €{selected_product['price']}")
            st.info(f"**Category:** {selected_product['category']}")
            if selected_product.get('key_features'):
                st.info(f"**Features:** {selected_product['key_features']}")
            
            # AI Status indicator
            if use_ai and api_key:
                st.success("🤖 AI Generation: Enabled")
            else:
                st.info("📝 Template Generation: Enabled")
                
        else:
            if not check and selected_product.get("name"):
                st.warning(error)
            else:
                st.warning("Select or enter product details to see preview")
    
    with col2:
        st.header("📱 Generated Ad Copies")
        
        if generate_button and can_generate and check:
            # Show loading spinner
            loading_message = "🤖 AI is crafting compelling ad copies..." if use_ai else "🔄 Generating compelling ad copies..."
            with st.spinner(loading_message):
                time.sleep(2.0 if use_ai else 1.5)  # Longer wait for AI
                copies = generator.generate_copies(selected_product, use_ai, api_key)
                st.session_state.generated_copies = copies
                st.session_state.generation_mode = "AI" if use_ai else "Template"
        
        # Display generated copies
        if 'generated_copies' in st.session_state:
            copies = st.session_state.generated_copies
            generation_mode = st.session_state.get('generation_mode', 'Template')
            
            # Show generation method
            if generation_mode == "AI":
                st.success("🤖 Generated using AI (Llama3 via Groq)")
            else:
                st.info("📝 Generated using templates")
            
            # Export options
            col_export1, col_export2 = st.columns(2)
            with col_export1:
                txt_export = generator.export_to_txt(copies)
                st.download_button(
                    label="📄 Download as TXT",
                    data=txt_export,
                    file_name=f"ai_facebook_ads_copy_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
            
            with col_export2:
                csv_export = generator.export_to_csv(copies)
                st.download_button(
                    label="📊 Download as CSV",
                    data=csv_export,
                    file_name=f"ai_facebook_ads_copy_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            
            # Display copies in tabs
            tab_names = []
            for copy in copies:
                ai_indicator = " 🤖" if copy.get('ai_generated', False) else " 📝"
                tab_names.append(f"{copy['style']}{ai_indicator}")
            
            tabs = st.tabs(tab_names)
            
            for tab, copy in zip(tabs, copies):
                with tab:
                    # AI generation indicator
                    if copy.get('ai_generated', False):
                        st.success("🤖 AI Generated Copy")
                    else:
                        st.info("📝 Template Based Copy")
                    
                    st.markdown(f"### {copy['style']} Style")
                    
                    # Headline
                    st.markdown("**📢 Headline**")
                    st.info(copy['headline'])
                    
                    # Primary text
                    st.markdown("**📝 Primary Text**")
                    st.success(copy['primary'])
                    
                    # CTA
                    st.markdown("**🔔 Call to Action**")
                    st.warning(copy['cta'])
                    
                    # Hashtags
                    st.markdown("**#️⃣ Hashtags**")
                    st.code(copy['hashtags'])
                    
                    # Copy to clipboard button
                    full_copy = f"{copy['headline']}\n\n{copy['primary']}\n\n{copy['cta']}\n\n{copy['hashtags']}"
                    st.text_area(
                        "Complete Ad Copy (click to select all):",
                        full_copy,
                        height=150,
                        key=f"copy_{copy['style']}_{copy.get('ai_generated', 'template')}"
                    )
        
        elif generate_button:
            if use_ai and not api_key:
                st.error("🔑 Please enter your Groq API key to use AI generation.")
            else:
                st.error("Please fill in all required product details before generating copies.")

    # Footer
    st.markdown("---")
    col_footer1, col_footer2 = st.columns(2)
    
    with col_footer1:
        st.markdown("**AI Facebook Ads Copy Generator** - Created for Vigoshop.si")
        st.markdown("Built with ❤️ using Python, Streamlit & Groq AI")
    
    with col_footer2:
        st.markdown("**Free AI Integration:**")
        st.markdown("• [Get Groq API Key](https://console.groq.com/) (Free)")
        st.markdown("• Powered by Llama3-8B model")
    
    st.warning("⚠️ Note: This is a prototype app using sample Vigoshop products. It is intended for demonstration purposes only.")

if __name__ == "__main__":
    main()
    