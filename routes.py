from flask import Flask, render_template,jsonify, session, url_for, request, Blueprint, flash,redirect, make_response
from models import db, Influencer, Sponsor, Admin, Campaign, AdRequest
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
from io import BytesIO
import calendar
from math import isnan 
import numpy as np


main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    if "spon_id" in session:
        return redirect(url_for("main.sponsor_dashboard"))
    elif "inf_id" in session:
        return redirect(url_for("main.influencer_dashboard"))
    elif "admin_id" in session:
        return redirect(url_for("main.admin_dashboard"))

    return render_template("home.html")

@main_bp.route("/login_admin", methods=["POST", "GET"])
def login_admin():
    error = None
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        admin = Admin.query.filter_by(email=email).first()
        if admin and admin.password == password:
            session["admin_id"] = admin.id
            return redirect(url_for("main.home"))
        else:
            error = "Invalid email or password."

    return render_template("login_admin.html", error=error)

@main_bp.route("/signup_influencer", methods =["GET","POST"])
def signup_influencer():
    error = None
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        reach = request.form["reach"]
        password = request.form["password"]
        niche = request.form["niche"]
        category = request.form["category"]

        inf = Influencer.query.filter_by(email = email).first()
        if inf:
            error = "Email address is already registered."
        else:
            new_inf = Influencer(name = name, email=email,password=password,niche=niche,category=category,reach=reach)
            db.session.add(new_inf)
            db.session.commit()
            return redirect( url_for("main.login_user"))

    return render_template("signup_influencer.html", error = error)

@main_bp.route("/signup_sponsor",methods =["GET", "POST"])
def signup_sponsor():
    error = None
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        budget = request.form["budget"]

        industry = request.form["industry"]
        password = request.form["password"]

        error = None
        spon = Sponsor.query.filter_by(email = email).first()
        if spon:
            error = "Email address is already registered."
        else:
            new_inf = Sponsor(name = name, email=email,password=password,budget=budget, industry = industry)
            db.session.add(new_inf)
            db.session.commit()
            return redirect(url_for("main.login_user"))

    return render_template("signup_sponsor.html", error=error)

@main_bp.route("/login_user", methods = ["POST", "GET"])
def login_user():
    error = None
    if request.method == "POST":
        type = request.form["type"]
        email = request.form["email"]
        password = request.form["password"]

        error = None
        if type == "influencer":
            inf = Influencer.query.filter_by(email = email).first()
            if inf and inf.password == password:
                session["inf_id"] = inf.id
                return redirect(url_for("main.home"))
            else:
                error = "Invalid email id or password."
        elif type == "sponsor":
            spon = Sponsor.query.filter_by(email = email).first()
            if spon and spon.password == password:
                session["spon_id"] = spon.id
                return redirect(url_for("main.home"))
            else:
                error = "Invalid email id or password."

    return render_template("login_user.html", error=error)

@main_bp.route("/sponsor_dashboard", methods=["GET", "POST"])
def sponsor_dashboard():

    if "spon_id" in session:
        spon = Sponsor.query.get(session["spon_id"])
    else:
        return redirect(url_for("main.login_user"))
    if spon.flagged:
        return render_template("user_flagged.html")
    campaigns = Campaign.query.filter_by(sponsor_id=spon.id,flagged=False).order_by(Campaign.id.desc()).all()
    for campaign in Campaign.query.all():
        campaign.progress = calculate_progress(campaign.start_date, campaign.end_date)
    db.session.commit()
    adrequests = AdRequest.query.filter_by(flagged=False).filter(
        AdRequest.campaign_id.in_([c.id for c in campaigns])
    ).order_by(AdRequest.id.desc()).all()
    influencers = Influencer.query.filter_by(flagged=False).all()

    total_campaigns = len(campaigns)
    public_campaigns = len([c for c in campaigns if c.visibility == 'public'])
    private_campaigns = len([c for c in campaigns if c.visibility == 'private'])
    total_ad_requests = len(adrequests)
    accepted_requests = AdRequest.query.filter(
        AdRequest.campaign_id.in_([c.id for c in campaigns]),AdRequest.status=='Accepted'
    ).count()
    rejected_requests = AdRequest.query.filter(
        AdRequest.campaign_id.in_([c.id for c in campaigns]),AdRequest.status=='Rejected'
    ).count()
    pending_requests = AdRequest.query.filter(
        AdRequest.campaign_id.in_([c.id for c in campaigns]),AdRequest.status=='Pending'
    ).count()

    money_spent = sum(ad.payment_amount if not ad.negotiation else ad.negotiation_amt for ad in  AdRequest.query.filter(
        AdRequest.campaign_id.in_([c.id for c in campaigns]),AdRequest.status=='Accepted'
    ))

    sent_requests = AdRequest.query.filter(AdRequest.campaign_id.in_([c.id for c in campaigns]), AdRequest.for_who == 'influencer').count()
    received_requests = AdRequest.query.filter(AdRequest.campaign_id.in_([c.id for c in campaigns]), AdRequest.for_who == 'sponsor').count()

    def create_pie_chart(labels, sizes, colors):
        if not sizes or sum(sizes) == 0:

            labels = ['No Data']
            sizes = [1]
            colors = ['grey']

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        ax.axis('equal')  

        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img_data = base64.b64encode(buf.getvalue()).decode('utf8')
        plt.close(fig)  
        return img_data

    campaign_visibility_data = {
        'Public': Campaign.query.filter_by(sponsor_id=spon.id, visibility='public').count(),
        'Private': Campaign.query.filter_by(sponsor_id=spon.id, visibility='private').count()
    }
    campaign_visibility_chart = create_pie_chart(
        list(campaign_visibility_data.keys()),
        list(campaign_visibility_data.values()),
        ['#36A2EB', '#FF6384']
    )

    ad_request_status_data = {
        'Pending': AdRequest.query.filter(AdRequest.campaign_id.in_([c.id for c in campaigns]), AdRequest.status == 'Pending').count(),
        'Accepted': AdRequest.query.filter(AdRequest.campaign_id.in_([c.id for c in campaigns]), AdRequest.status == 'Accepted').count(),
        'Rejected': AdRequest.query.filter(AdRequest.campaign_id.in_([c.id for c in campaigns]), AdRequest.status == 'Rejected').count()
    }
    ad_request_status_chart = create_pie_chart(
        list(ad_request_status_data.keys()),
        list(ad_request_status_data.values()),
        ['#FFCE56', '#4BC0C0', '#FF6384']
    )

    categories = db.session.query(Influencer.category).distinct().all()
    adreq_dict = {campaignn.id: AdRequest.query.filter_by(campaign_id=campaignn.id).order_by(AdRequest.id.desc()).first() for campaignn in Campaign.query.filter_by(sponsor_id=spon.id).all()}

    if request.method == "POST":
        if 'campaign_name' in request.form:

            campaign_name = request.form.get('campaign_name')

            influencer_category = request.form.get('influencer_category')
            min_budget = request.form.get('min_budget')
            max_budget = request.form.get('max_budget')
            visibility = request.form.get('visibility')
            ad_influencer_name = request.form.get('ad_influencer_name')
            payment_amount = request.form.get('payment_amount')
            ad_status = request.form.get('ad_status')
            ad_sent = request.form.get('ad_sent')

            filtered_campaigns = Campaign.query.filter_by(sponsor_id=session.get("spon_id"),flagged=False)
            if campaign_name:
                filtered_campaigns = filtered_campaigns.filter(Campaign.name.ilike(f'%{campaign_name}%'))

            if min_budget:
                filtered_campaigns = filtered_campaigns.filter(Campaign.budget >= min_budget)
            if max_budget:
                filtered_campaigns = filtered_campaigns.filter(Campaign.budget <= max_budget)
            if visibility:
                filtered_campaigns = filtered_campaigns.filter(Campaign.visibility == visibility)

            filtered_campaigns = filtered_campaigns.order_by(Campaign.id.desc()).all()

            filtered_adrequests = AdRequest.query

            if ad_influencer_name:
                filtered_adrequests = filtered_adrequests.join(Campaign).join(Influencer).filter(Influencer.name.ilike(f'%{ad_influencer_name}%'))
            if payment_amount:
                filtered_adrequests = filtered_adrequests.filter(AdRequest.payment_amount == payment_amount)

            if ad_status:
                filtered_adrequests = filtered_adrequests.filter(AdRequest.status == ad_status)
            current_user_id = session.get("spon_id")
            if ad_sent == 'sent':

                filtered_adrequests = (filtered_adrequests
                                    .join(Campaign)
                                    .filter(Campaign.sponsor_id == current_user_id)
                                    .filter(AdRequest.for_who == 'influencer'))
            elif ad_sent == 'received':

                filtered_adrequests = (filtered_adrequests
                                    .join(Campaign)
                                    .filter(Campaign.sponsor_id == current_user_id)
                                    .filter(AdRequest.for_who == 'sponsor'))
            filtered_adrequests = filtered_adrequests.filter_by(flagged=False).order_by(AdRequest.id.desc()).all()

            return render_template('sponsor_dashboard.html', 
                                   user = spon,
                                    campaigns=campaigns, 
                                    adrequests=adrequests, 
                                    influencers=influencers, 
                                    categories=[c[0] for c in categories],
                                    adreq_dict=adreq_dict,
                                    filtered_campaigns= filtered_campaigns,
                                    filtered_adrequests=filtered_adrequests,total_campaigns=total_campaigns,
                           public_campaigns=public_campaigns,
                           private_campaigns=private_campaigns,
                           total_ad_requests=total_ad_requests,
                           accepted_requests=accepted_requests,
                           rejected_requests=rejected_requests,
                           pending_requests=pending_requests,
                           money_spent=money_spent,
                           sent_requests=sent_requests,
                           received_requests=received_requests,
                           campaign_visibility_chart=campaign_visibility_chart,
                           ad_request_status_chart=ad_request_status_chart)

        else:

            name = request.form['name']
            description = request.form['description']
            budget = request.form['budget']
            if int(budget) > spon.budget:
                return redirect(url_for('main.sponsor_dashboard'))
            start_date_str = request.form['start_date']
            end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d')
            visibility = request.form['visibility']
            if request.form['message']:
                message = request.form['message']
            else:
                message = 'Ad request message'
            if request.form['requirements']:
                req = request.form['requirements']
            else:
                req = 'Ad request requirements'
            goals = request.form['goals']
            selected_influencer_id = request.form.get('selectedInfluencer')

            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            if start_date.date() == datetime.now().date():
                start_date = datetime.now()

            sponsor_id = session.get("spon_id")
            if sponsor_id is None:
                flash('Sponsor ID not found in session. Please log in again.', 'error')
                return redirect(url_for('main.login_user'))

            new_campaign = Campaign(
                name=name,
                description=description,
                budget=budget,
                start_date=start_date,
                end_date=end_date,
                visibility=visibility,
                goals=goals,
                sponsor_id=sponsor_id,
                progress=0
            )
            db.session.add(new_campaign)
            db.session.commit()

            if visibility == 'private' and selected_influencer_id:
                new_ad_request = AdRequest(
                    campaign_id=new_campaign.id,
                    influencer_id=selected_influencer_id,

                    message=message,
                    requirements=req,
                    payment_amount=int(budget),
                    status='Pending'
                )
                db.session.add(new_ad_request)
                db.session.commit()

            return redirect(url_for('main.sponsor_dashboard'))

    return render_template("sponsor_dashboard.html", 
                           user=spon, 
                           campaigns=campaigns, 
                           adrequests=adrequests, 
                           influencers=influencers, 
                           categories=[c[0] for c in categories],
                           adreq_dict=adreq_dict,
                           total_campaigns=total_campaigns,
                           public_campaigns=public_campaigns,
                           private_campaigns=private_campaigns,
                           total_ad_requests=total_ad_requests,
                           accepted_requests=accepted_requests,
                           rejected_requests=rejected_requests,
                           pending_requests=pending_requests,
                           money_spent=money_spent,
                           sent_requests=sent_requests,
                           received_requests=received_requests,
                           campaign_visibility_chart=campaign_visibility_chart,
                           ad_request_status_chart=ad_request_status_chart)

def calculate_progress(start_date, end_date):
    total_duration = (end_date - start_date).total_seconds() /(60*60)
    elapsed_duration = (datetime.now() - start_date).total_seconds() /(60*60)
    if total_duration == 0:
        return 100
    return round(min(100, max(0, (elapsed_duration / total_duration) * 100)),2)

@main_bp.route('/view_influencer_profile/<int:influencer_id>')
def view_influencer_profile(influencer_id):
    influencer = Influencer.query.get_or_404(influencer_id)
    accepted_campaigns = AdRequest.query.filter_by(influencer_id=influencer.id, status='Accepted').count()
    return jsonify({
        'name': influencer.name,
        'email': influencer.email,
        'category': influencer.category,
        'niche': influencer.niche,
        'reach': influencer.reach,
        'balance': influencer.balance,
        'accepted_campaigns': accepted_campaigns
    })

@main_bp.route("/update_campaign/<int:campaign_id>", methods=["POST"])
def update_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    campaign.name = request.form['name']
    campaign.description = request.form['description']
    campaign.start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d')
    campaign.end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d')
    campaign.budget = request.form['budget']
    campaign.visibility = request.form['visibility']
    campaign.goals = request.form['goals']

    db.session.commit()
    return redirect(url_for('main.sponsor_dashboard'))

@main_bp.route("/accept_ad_request/<int:ad_request_id>", methods=["POST"])
def accept_ad_request(ad_request_id):
    ad_request = AdRequest.query.get_or_404(ad_request_id)
    ad_request.status = "Accepted"
    ad_request.campaign.stat = "Active"
    if ad_request.negotiation:
        ad_request.influencer.balance += ad_request.negotiation_amt
        ad_request.campaign.sponsor.budget -= ad_request.negotiation_amt
        ad_request.campaign.budget = ad_request.negotiation_amt

    else:
        ad_request.influencer.balance += ad_request.payment_amount
        ad_request.campaign.sponsor.budget -= ad_request.payment_amount
        ad_request.campaign.budget = ad_request.payment_amount

    db.session.commit()
    return redirect(url_for('main.home'))

@main_bp.route("/reject_ad_request/<int:ad_request_id>", methods=["POST"])
def reject_ad_request(ad_request_id):
    ad_request = AdRequest.query.get_or_404(ad_request_id)
    ad_request.status = "Rejected"
    if ad_request.campaign.visibility== "private":
        ad_request.campaign.stat = "Inactive"
    db.session.commit()
    return redirect(url_for('main.home'))

@main_bp.route("/negotiate_ad_request/<int:ad_request_id>", methods=["POST"])
def negotiate_ad_request(ad_request_id):
    ad_request = AdRequest.query.get_or_404(ad_request_id)
    ad_request.for_who = "influencer"
    ad_request.negotiation= True
    ad_request.negotiation_amt = request.form['negotiation_amount']
    db.session.commit()
    return redirect(url_for('main.home'))

@main_bp.route("/negotiate_inf_ad_request/<int:ad_request_id>", methods=["POST"])
def negotiate_inf_ad_request(ad_request_id):
    ad_request = AdRequest.query.get_or_404(ad_request_id)
    ad_request.for_who = "sponsor"
    ad_request.negotiation= True
    ad_request.negotiation_amt = request.form['negotiation_amount']
    db.session.commit()
    return redirect(url_for('main.home'))

@main_bp.route("/new_ad_request/<int:adreqid>", methods=["POST"])
def new_ad_request(adreqid):
    adreq = AdRequest.query.get(adreqid)
    adreq.negotiation = False
    adreq.negotiation_amt =0
    adreq.for_who= "influencer"
    adreq.status = "Pending"
    adreq.influencer_id = request.form['new_influencer_id']

    db.session.commit()
    return redirect(url_for('main.sponsor_dashboard'))

@main_bp.route('/send_ad_request', methods=['POST'])
def send_ad_request():
    campaign_id = request.form['campaign_id']
    influencer_id = request.form['influencer_id']
    message = request.form['message']
    requirements = request.form['requirements']
    payment_amount = request.form['payment_amount']

    new_ad_request = AdRequest(
        campaign_id=campaign_id,
        influencer_id=influencer_id,
        message=message,
        requirements=requirements,
        payment_amount=payment_amount,
        status='Pending'
    )
    db.session.add(new_ad_request)
    db.session.commit()

    return redirect(url_for('main.sponsor_dashboard'))

@main_bp.route("/influencer_dashboard", methods=['GET', 'POST'])
def influencer_dashboard():
    if "inf_id" in session:
        inf = Influencer.query.get(session["inf_id"])
    else:
        return redirect(url_for("main.login_user")) 

    if inf.flagged:
        return render_template("user_flagged.html")

    adrequests = AdRequest.query.filter_by(influencer_id=inf.id,flagged=False).order_by(AdRequest.id.desc()).all()
    adreqs = AdRequest.query.filter_by(influencer_id=inf.id, status="Accepted",flagged=False).all()
    campaigns = Campaign.query.filter_by(flagged=False).filter(Campaign.id.in_([adreq.campaign.id for adreq in adreqs])).distinct(Campaign.id).order_by(Campaign.id.desc()).all()
    camps = Campaign.query.filter_by(flagged=False).order_by(Campaign.id.desc()).all()

    adreq_dict = {campaign.id: AdRequest.query.filter_by(campaign_id=campaign.id, influencer_id=inf.id,flagged=False).first() for campaign in camps}

    for campaign in Campaign.query.all():
        campaign.progress = calculate_progress(campaign.start_date, campaign.end_date)

    db.session.commit()

    filtered_campaigns = []
    filtered_adrequests = []

    total_campaigns = len(campaigns)
    accepted_requests = AdRequest.query.filter_by(influencer_id=inf.id, status="Accepted").count()
    pending_requests = AdRequest.query.filter_by(influencer_id=inf.id, status="Pending").count()
    rejected_requests = AdRequest.query.filter_by(influencer_id=inf.id, status="Rejected").count()

    total_earnings = inf.balance

    def generate_pie_chart():
        img = io.BytesIO()
        labels = 'Accepted', 'Pending', 'Rejected'
        sizes = [accepted_requests, pending_requests, rejected_requests]
        colors = ['green', 'orange', 'red']

        if sum(sizes) == 0:
            sizes = [1, 1, 1]
            labels = ['Accepted (No Data)', 'Pending (No Data)', 'Rejected (No Data)']

        plt.figure(figsize=(6, 6))
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')
        plt.title('Ad Requests Status Distribution')
        plt.savefig(img, format='png')
        plt.close()
        img.seek(0)
        return base64.b64encode(img.getvalue()).decode('utf8')

    def generate_visibility_bar_chart():
        img = io.BytesIO()
        public_campaigns = db.session.query(Campaign).join(AdRequest)\
            .filter_by(flagged=False).filter(Campaign.visibility == 'public', AdRequest.influencer_id == inf.id, AdRequest.status == 'Accepted').count()
        private_campaigns = db.session.query(Campaign).join(AdRequest)\
            .filter_by(flagged=False).filter(Campaign.visibility == 'private', AdRequest.influencer_id == inf.id, AdRequest.status == 'Accepted').count()
        labels = ['Public', 'Private']
        sizes = [public_campaigns, private_campaigns]

        plt.figure(figsize=(8, 6))
        plt.bar(labels, sizes, color=['blue', 'grey'])
        plt.title('Campaigns by Visibility')
        plt.xlabel('Visibility')
        plt.ylabel('Number of Campaigns')
        plt.savefig(img, format='png')
        plt.close()
        img.seek(0)
        return base64.b64encode(img.getvalue()).decode('utf8')

    def generate_monthly_earnings_bar_chart(inf_id):
        img = io.BytesIO()

        ad_requests = AdRequest.query.filter_by(influencer_id=inf_id, status="Accepted", flagged=False).all()

        monthly_earnings = {month: 0 for month in range(1, 13)}

        for ad_request in ad_requests:
            month = ad_request.campaign.start_date.month
            monthly_earnings[month] += ad_request.payment_amount

        months = [calendar.month_abbr[month] for month in monthly_earnings.keys()]
        earnings = list(monthly_earnings.values())

        plt.figure(figsize=(10, 6))
        plt.bar(months, earnings, color='blue')
        plt.title('Monthly Earnings')
        plt.xlabel('Month')
        plt.ylabel('Earnings')
        plt.savefig(img, format='png')
        plt.close()
        img.seek(0)
        return base64.b64encode(img.getvalue()).decode('utf8')

    pie_chart = generate_pie_chart()
    monthly_earnings_bar_chart = generate_monthly_earnings_bar_chart(session["inf_id"])
    bar_chart = generate_visibility_bar_chart()

    industries = Sponsor.query.with_entities(Sponsor.industry).distinct().all()
    industries = [industry[0] for industry in industries if industry[0]]  

    if request.method == 'POST':

        campaign_name = request.form.get('campaign_name')
        sponsor_name = request.form.get('sponsor_name')
        sponsor_industry = request.form.get('sponsor_industry')
        min_budget = request.form.get('min_budget', type=float)
        max_budget = request.form.get('max_budget', type=float)
        visibility = request.form.get('visibility')
        ad_sponsor_name = request.form.get('ad_sponsor_name')
        payment_amount = request.form.get('payment_amount', type=float)
        ad_status = request.form.get('ad_status')
        ad_sent = request.form.get('ad_sent')

        filtered_campaigns_query = Campaign.query.join(Sponsor).filter_by(flagged=False).filter(
            (Campaign.visibility == 'public') |
            (Campaign.id.in_([adreq.campaign_id for adreq in adrequests])))

        if campaign_name:
            filtered_campaigns_query = filtered_campaigns_query.filter(Campaign.name.ilike(f'%{campaign_name}%'))
        if sponsor_name:
            filtered_campaigns_query = filtered_campaigns_query.filter(Sponsor.name.ilike(f'%{sponsor_name}%'))
        if sponsor_industry:
            filtered_campaigns_query = filtered_campaigns_query.filter(Sponsor.industry == sponsor_industry)
        if min_budget is not None:
            filtered_campaigns_query = filtered_campaigns_query.filter(Campaign.budget >= min_budget)
        if max_budget is not None:
            filtered_campaigns_query = filtered_campaigns_query.filter(Campaign.budget <= max_budget)
        if visibility:
            filtered_campaigns_query = filtered_campaigns_query.filter(Campaign.visibility == visibility)

        filtered_campaigns = filtered_campaigns_query.order_by(Campaign.id.desc()).all()

        filtered_adrequests_query = AdRequest.query.join(Campaign).join(Sponsor).filter_by(flagged=False).filter(AdRequest.campaign_id == Campaign.id, AdRequest.influencer_id == inf.id)

        if ad_sponsor_name:
            filtered_adrequests_query = filtered_adrequests_query.filter(Sponsor.name.ilike(f'%{ad_sponsor_name}%'))
        if payment_amount is not None:
            filtered_adrequests_query = filtered_adrequests_query.filter(AdRequest.payment_amount == payment_amount)
        if ad_status:
            filtered_adrequests_query = filtered_adrequests_query.filter(AdRequest.status == ad_status)
        if ad_sent == "received":
            filtered_adrequests_query = filtered_adrequests_query.filter(AdRequest.for_who == "influencer")
        elif ad_sent == "sent":
            filtered_adrequests_query = filtered_adrequests_query.filter(AdRequest.for_who == "sponsor")

        filtered_adrequests = filtered_adrequests_query.order_by(AdRequest.id.desc()).all()

    return render_template("influencer_dashboard.html", user=inf, adrequests=adrequests, campaigns=campaigns, camps=camps, adreq_dict=adreq_dict, filtered_campaigns=filtered_campaigns, filtered_adrequests=filtered_adrequests, industries=industries, total_campaigns=total_campaigns, accepted_requests=accepted_requests, pending_requests=pending_requests, rejected_requests=rejected_requests, total_earnings=total_earnings, bar_chart=bar_chart,pie_chart=pie_chart,monthly_earnings_bar_chart=monthly_earnings_bar_chart)

@main_bp.route("/edit_inf_profile", methods=["POST"])
def edit_inf_prof():
    if "inf_id" in session:
        inf = Influencer.query.get(session["inf_id"])
    else:
        return redirect(url_for("main.login_user"))
        inf = Influencer.query.get(1)  
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]
        reach = request.form["reach"]
        category = request.form["category"]
        niche = request.form["niche"]

        inf.name = name
        if password != "":
            inf.password = password
        inf.reach = reach
        inf.category = category
        inf.niche = niche

        db.session.commit()

        return redirect(url_for("main.influencer_dashboard"))

@main_bp.route("/edit_profile", methods=["POST"])
def edit_prof():
    if "spon_id" in session:
        spon = Sponsor.query.get(session["spon_id"])
    else:
        spon = Sponsor.query.get(1)  
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]
        age = request.form["age"]
        budget = request.form["budget"]
        industry = request.form["industry"]
        spon = Sponsor.query.get(session["spon_id"])
        spon.name = name
        if password != "":
            spon.password = password
        spon.age = age
        spon.industry = industry
        spon.budget = budget

        db.session.commit()

        return redirect(url_for("main.sponsor_dashboard"))

@main_bp.route("/delete_ad_request/<int:ad_request_id>", methods = ["POST"])
def delete_ad_request(ad_request_id):
    adreq = AdRequest.query.get(ad_request_id)
    db.session.delete(adreq)
    db.session.commit()
    return redirect(url_for("main.home"))

@main_bp.route("/delete_campaign/<int:campaign_id>", methods = ["POST"])
def delete_campaign(campaign_id):
    camp = Campaign.query.get(campaign_id)
    for adreq in AdRequest.query.filter(AdRequest.campaign_id == campaign_id).all():
        db.session.delete(adreq)
    db.session.delete(camp)
    db.session.commit()
    return redirect(url_for("main.home"))

@main_bp.route("/public_send_req/<int:camp_id>", methods=["POST"])
def public_send_req(camp_id):
    if request.method == "POST":
        campaign = Campaign.query.get(camp_id)
        if request.form["negotiation_amount"] != "":
            adreq = AdRequest(campaign_id = camp_id, influencer_id = session["inf_id"],negotiation = True, negotiation_amt = request.form["negotiation_amount"], for_who="sponsor", status="Pending", message="Hire me and I will promote your product.", requirements=campaign.goals, payment_amount = campaign.budget)
        else:
            adreq = AdRequest(campaign_id = camp_id, influencer_id = session["inf_id"],negotiation = False, for_who="sponsor", status="Pending", message="Hire me and I will promote your product.",  requirements=campaign.goals, payment_amount = campaign.budget)

        db.session.add(adreq)
        db.session.commit()
    return redirect(url_for("main.influencer_dashboard"))

@main_bp.route('/add_money', methods=['POST'])
def add_money():
    if "spon_id" in session:
        spon = Sponsor.query.get(session["spon_id"])
    else:

        return redirect(url_for('main.login_user'))

    card_number = request.form['cardNumber']
    expiry_date = request.form['expiryDate']
    cvv = request.form['cvv']
    amount = float(request.form['amount'])

    if len(card_number) == 16 and len(cvv) == 3 and '/' in expiry_date:

        spon.budget += amount
        db.session.commit()

    return redirect(url_for('main.sponsor_dashboard'))


@main_bp.route('/admin_dashboard')
def admin_dashboard():
    if "admin_id" not in session:
        return redirect(url_for("main.login_admin"))

    # Fetch data from the database
    campaigns = Campaign.query.all()
    influencers = Influencer.query.all()
    sponsors = Sponsor.query.all()
    adrequests = AdRequest.query.all()

    # Ensure the counts are valid even if the database is empty
    total_campaigns = len(campaigns) if campaigns else 0
    total_influencers = len(influencers) if influencers else 0
    total_sponsors = len(sponsors) if sponsors else 0
    total_adrequests = len(adrequests) if adrequests else 0

    # Ensure counts are safe for empty results
    accepted_adrequests = AdRequest.query.filter_by(status='Accepted').count() if total_adrequests > 0 else 0
    rejected_adrequests = AdRequest.query.filter_by(status='Rejected').count() if total_adrequests > 0 else 0
    pending_adrequests = AdRequest.query.filter_by(status='Pending').count() if total_adrequests > 0 else 0
    public_campaigns = Campaign.query.filter_by(visibility='public').count() if total_campaigns > 0 else 0
    private_campaigns = Campaign.query.filter_by(visibility='private').count() if total_campaigns > 0 else 0

    # Handle total budget safely for empty data
    total_budget_used = db.session.query(Campaign).join(Campaign.ad_requests) \
        .filter(AdRequest.status == 'Accepted').distinct().with_entities(Campaign.budget).all()

    total_budget_used = sum(budget for (budget,) in total_budget_used if budget is not None)
    if np.isnan(total_budget_used) or total_budget_used < 0:
        total_budget_used = 0

    # Plot graphs with zero-safe values

    # 1. Statistics Bar Graph (Campaigns, Influencers, Sponsors, Ad Requests)
    statistics_img = io.BytesIO()
    fig, ax = plt.subplots()
    labels = ['Campaigns', 'Influencers', 'Sponsors', 'Ad Requests']
    sizes = [total_campaigns, total_influencers, total_sponsors, total_adrequests]

    sizes = np.nan_to_num(sizes)  # Ensure NaN is converted to 0
    ax.bar(labels, sizes)
    ax.set_ylabel('Count')
    plt.savefig(statistics_img, format='png')
    plt.close(fig)
    statistics_img.seek(0)
    statistics_img_data = base64.b64encode(statistics_img.getvalue()).decode('utf-8')

    # 2. Ad Requests Status Pie Chart (Accepted, Rejected, Pending)
    ad_requests_img = io.BytesIO()
    fig, ax = plt.subplots()
    labels = ['Accepted', 'Rejected', 'Pending']
    sizes = [accepted_adrequests, rejected_adrequests, pending_adrequests]

    sizes = np.array(sizes)
    sizes = np.nan_to_num(sizes)  # Convert NaN to 0

    # Check if all sizes are zero
    if np.sum(sizes) > 0:
        autopct = '%1.1f%%'  # Only show percentages if there's data
    else:
        autopct = None

    ax.pie(sizes, labels=labels, autopct=autopct, startangle=140)
    ax.axis('equal')
    plt.savefig(ad_requests_img, format='png')
    plt.close(fig)
    ad_requests_img.seek(0)
    ad_requests_img_data = base64.b64encode(ad_requests_img.getvalue()).decode('utf-8')

    # 3. Campaigns Visibility Pie Chart (Public, Private)
    campaigns_visibility_img = io.BytesIO()
    fig, ax = plt.subplots()
    labels = ['Public', 'Private']
    sizes = [public_campaigns, private_campaigns]

    sizes = np.array(sizes)
    sizes = np.nan_to_num(sizes)  # Convert NaN to 0

    # Check if all sizes are zero
    if np.sum(sizes) > 0:
        autopct = '%1.1f%%'  # Only show percentages if there's data
    else:
        autopct = None

    ax.pie(sizes, labels=labels, autopct=autopct, startangle=140)
    ax.axis('equal')
    plt.savefig(campaigns_visibility_img, format='png')
    plt.close(fig)
    campaigns_visibility_img.seek(0)
    campaigns_visibility_img_data = base64.b64encode(campaigns_visibility_img.getvalue()).decode('utf-8')

    # 4. Budget Usage Bar Chart
    budget_usage_img = io.BytesIO()
    fig, ax = plt.subplots()

    total_budget_used = total_budget_used if total_budget_used >= 0 else 0  # Ensure it's non-negative

    ax.bar(['Total Budget Used'], [total_budget_used])
    ax.set_ylabel('Budget')
    plt.savefig(budget_usage_img, format='png')
    plt.close(fig)
    budget_usage_img.seek(0)
    budget_usage_img_data = base64.b64encode(budget_usage_img.getvalue()).decode('utf-8')

    return render_template('admin_dashboard.html',
                           campaigns=campaigns,
                           influencers=influencers,
                           sponsors=sponsors,
                           adrequests=adrequests,
                           total_campaigns=total_campaigns,
                           total_influencers=total_influencers,
                           total_sponsors=total_sponsors,
                           total_adrequests=total_adrequests,
                           accepted_adrequests=accepted_adrequests,
                           rejected_adrequests=rejected_adrequests,
                           pending_adrequests=pending_adrequests,
                           public_campaigns=public_campaigns,
                           private_campaigns=private_campaigns,
                           total_budget_used=total_budget_used,
                           statistics_img=statistics_img_data,
                           ad_requests_img=ad_requests_img_data,
                           campaigns_visibility_img=campaigns_visibility_img_data,
                           budget_usage_img=budget_usage_img_data)



@main_bp.route('/admin_dashboard/<item_type>_details/<int:item_id>')
def item_details(item_type, item_id):
    if 'admin_id' in session:
        if item_type == 'campaign':
            item = Campaign.query.get(item_id)
            details = render_template('campaign_details.html', campaign=item)
        elif item_type == 'influencer':
            item = Influencer.query.get(item_id)
            details = render_template('influencer_details.html', influencer=item)
        elif item_type == 'sponsor':
            item = Sponsor.query.get(item_id)
            details = render_template('sponsor_details.html', sponsor=item)
        elif item_type == 'adrequest':
            item = AdRequest.query.get(item_id)
            details = render_template('adrequest_details.html', adrequest=item)
        return details
    else:
        return redirect(url_for('main.login_admin'))

@main_bp.route('/admin_dashboard/toggle_flag/campaign/<int:item_id>', methods=['POST'])
def toggle_flag_campaign(item_id):
    campaign = Campaign.query.get(item_id)
    if campaign:
        campaign.flagged = not campaign.flagged

        for adreq in campaign.ad_requests:
            adreq.flagged = campaign.flagged
        db.session.commit()

    return redirect(url_for('main.admin_dashboard'))

@main_bp.route('/admin_dashboard/toggle_flag/influencer/<int:item_id>', methods=['POST'])
def toggle_flag_influencer(item_id):
    influencer = Influencer.query.get(item_id)
    if influencer:
        influencer.flagged = not influencer.flagged
        for adreq in influencer.ad_requests:
            adreq.flagged = influencer.flagged
        db.session.commit()

    return redirect(url_for('main.admin_dashboard'))

@main_bp.route('/admin_dashboard/toggle_flag/sponsor/<int:item_id>', methods=['POST'])
def toggle_flag_sponsor(item_id):
    sponsor = Sponsor.query.get(item_id)
    if sponsor:
        sponsor.flagged = not sponsor.flagged
        for campaign in sponsor.campaigns:
            campaign.flagged = sponsor.flagged
            for adreq in campaign.ad_requests:
                adreq.flagged = campaign.flagged

        db.session.commit()

    return redirect(url_for('main.admin_dashboard'))

@main_bp.route('/admin_dashboard/toggle_flag/adrequest/<int:item_id>', methods=['POST'])
def toggle_flag_adrequest(item_id):
    adrequest = AdRequest.query.get(item_id)
    if adrequest:
        adrequest.flagged = not adrequest.flagged
        db.session.commit()

    return redirect(url_for('main.admin_dashboard'))

@main_bp.route("/logout", methods=["POST","GET"])
def logout():
    session.clear()
    return redirect(url_for("main.home"))