document.addEventListener('DOMContentLoaded', function() {
    // Retrieve the saved section ID from localStorage
    const savedSectionId = localStorage.getItem('currentSection');

    // If there's a saved section, show it; otherwise, show the default 'profile' section
    if (savedSectionId) {
        showSection(savedSectionId);
    } else {
        showSection('profile');
    }
});

function showSection(sectionId) {
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => {
        section.classList.remove('active');
    });

    const buttons = document.querySelectorAll('#inlline button');
    buttons.forEach(button => {
        button.classList.remove('active');
    });

    document.getElementById(sectionId).classList.add('active');
    document.getElementById(sectionId + 'Button').classList.add('active');

    localStorage.setItem('currentSection', sectionId);
}

function logout(url) {
    window.location.href = url;
}

function openModal() {
    document.getElementById('addCampaignModal').style.display = 'block';
}
function openViewModalCC(campaignId) {
    document.getElementById('viewCampaignModalCC-' + campaignId).style.display = 'block';

}
function openViewModalCFS(campaignId) {
    document.getElementById('viewCampaignModalCFS-' + campaignId).style.display = 'block';

}

function closeViewCampaignModal(campaignId) {
    var modal = document.getElementById('viewCampaignModal-' + campaignId);
    modal.style.display = 'none';
}

function closeViewCampaignModalCF(campaignId) {
    var modal = document.getElementById('viewCampaignModalCF-' + campaignId);
    modal.style.display = 'none';
}

function closeViewCampaignModalCC(campaignId) {
    var modal = document.getElementById('viewCampaignModalCC-' + campaignId);
    modal.style.display = 'none';
}


function closeViewCampaignModalCFS(campaignId) {
    var modal = document.getElementById('viewCampaignModalCFS-' + campaignId);
    modal.style.display = 'none';
}

function openViewModal(campaignId) {
    document.getElementById('viewCampaignModal-' + campaignId).style.display = 'block';
}

function openViewModalCF(campaignId) {
    document.getElementById('viewCampaignModalCF-' + campaignId).style.display = 'block';
}



function closeViewModal(campaignId) {
    document.getElementById('viewCampaignModal-' + campaignId).style.display = 'none';
}

function closeModal() {
    document.getElementById('addCampaignModal').style.display = 'none';
}

function openInfluencerModal() {
    document.getElementById('influencerModal').style.display = 'block';
}

function closeInfluencerModal() {
    document.getElementById('influencerModal').style.display = 'none';
}

function toggleInfluencerSelection() {
    var visibility = document.getElementById('visibility').value;
    var influencerSelection = document.getElementById('influencerSelection');
    var message = document.getElementById('mess');
    var req = document.getElementById('reqs');
    var message2 = document.getElementById('mess2');
    var req2 = document.getElementById('reqs2');
    // var req = document.getElementById('reqs');
    if (visibility === 'private') {
        influencerSelection.style.display = 'block';
        message.style.display = 'block';
        req.style.display = 'block';
        message2.style.display = 'block';
        req2.style.display = 'block';
    } else {
        influencerSelection.style.display = 'none';
        message.style.display = 'none';
        req.style.display = 'none';
        message2.style.display = 'none';
        req2.style.display = 'none';
    }
}
// function toggleInfluencerSelectionN() {
//     var visibility = document.getElementById('visibilityN').value;
//     var influencerSelection = document.getElementById('influencerSelectionN');
//     if (visibility === 'private') {
//         influencerSelection.style.display = 'block';
//     } else {
//         influencerSelection.style.display = 'none';
//     }
// }


function filterInfluencersList() {
    var category = document.getElementById('categoryFilter').value;
    var influencerCards = document.querySelectorAll('.influencer-card');
    influencerCards.forEach(function (card) {
        if (category === "" || card.getAttribute('data-category') === category) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}
function viewProfile(influencerId) {
    fetch(`/view_influencer_profile/${influencerId}`)
        .then(response => response.json())
        .then(data => {
            var profileContent = `
        <p><strong>Name:</strong> ${data.name}</p>
        <p><strong>Email:</strong> ${data.email}</p>
        <p><strong>Category:</strong> ${data.category}</p>
        <p><strong>Niche:</strong> ${data.niche}</p>
        <p><strong>Reach:</strong> ${data.reach}</p>
        <p><strong>Balance:</strong> ${data.balance}</p>
        <p><strong>Accepted Campaigns:</strong> ${data.accepted_campaigns}</p>
    `;
            document.getElementById('profileContent').innerHTML = profileContent;
            document.getElementById('viewProfileModal').style.display = 'block';
        })
        .catch(error => {
            console.error('Error fetching profile:', error);
        });
}

function closeViewProfileModal() {
    document.getElementById('viewProfileModal').style.display = 'none';
}

function selectInfluencer(influencerId, influencerName) {
    document.getElementById('selectedInfluencer').value = influencerId;
    document.getElementById('selectedInfluencerName').textContent = influencerName;
    closeInfluencerModal();
}

function openAdRequestModal(adRequestId) {
    document.getElementById('viewAdRequestModal-' + adRequestId).style.display = 'block';
}
function openAdRequestModalCFS(adRequestId) {
    document.getElementById('viewAdRequestModalCFS-' + adRequestId).style.display = 'block';
}

function closeAdRequestModal(adRequestId) {
    document.getElementById('viewAdRequestModal-' + adRequestId).style.display = 'none';
}

function closeAdRequestModalCFS(adRequestId) {
    document.getElementById('viewAdRequestModalCFS-' + adRequestId).style.display = 'none';
}

function openAdRequestModalCF(adRequestId) {
    document.getElementById('viewAdRequestModalCF-' + adRequestId).style.display = 'block';
}

function closeAdRequestModalCF(adRequestId) {
    document.getElementById('viewAdRequestModalCF-' + adRequestId).style.display = 'none';
}

function openAdRequestModalC(adRequestId) {
    document.getElementById('viewAdRequestModalC-' + adRequestId).style.display = 'block';
}

function closeAdRequestModalC(adRequestId) {
    document.getElementById('viewAdRequestModalC-' + adRequestId).style.display = 'none';
}


function openSendAdRequestModal() {
    document.getElementById('sendAdRequestModal').style.display = 'block';
}

function closeSendAdRequestModal() {
    document.getElementById('sendAdRequestModal').style.display = 'none';
}

function filterCampaigns() {
    var input, filter, select, options, i;
    input = document.getElementById("campaignSearch");
    filter = input.value.toUpperCase();
    select = document.getElementById("campaignSelect");
    options = select.getElementsByTagName("option");
    for (i = 0; i < options.length; i++) {
        if (options[i].text.toUpperCase().indexOf(filter) > -1) {
            options[i].style.display = "";
        } else {
            options[i].style.display = "none";
        }
    }
}

function filterInfluencers() {
    var input, filter, select, options, i;
    input = document.getElementById("influencerSearch");
    filter = input.value.toUpperCase();
    select = document.getElementById("influencerSelect");
    options = select.getElementsByTagName("option");
    for (i = 0; i < options.length; i++) {
        if (options[i].text.toUpperCase().indexOf(filter) > -1) {
            options[i].style.display = "";
        } else {
            options[i].style.display = "none";
        }
    }
}

document.getElementById('addMoneyBtn').addEventListener('click', function() {
    document.getElementById('paymentPopupContainer').style.display = 'flex';
});

document.getElementById('paymentPopupClose').addEventListener('click', function() {
    document.getElementById('paymentPopupContainer').style.display = 'none';
});

window.onclick = function(event) {
    if (event.target == document.getElementById('paymentPopupContainer')) {
        document.getElementById('paymentPopupContainer').style.display = 'none';
    }
};

// function openPopupAdm(type, id) {
//     $.ajax({
//         url: `/admin_dashboard/${type}_details/${id}`,
//         method: 'GET',
//         success: function(data) {
//             $('#popup-details_adm').html(data);
//             $('#popup_adm').show();
//         }
//     });
// }

// function closePopupAdm() {
//     $('#popup_adm').hide();
// }

// function flagItem(type, id) {
//     $.ajax({
//         url: `/admin_dashboard/flag_${type}/${id}`,
//         method: 'POST',
//         success: function(data) {
//             alert(data.message);
//             // Reload the popup details
//             openPopupAdm(type, id);
//         }
//     });
// }

// Function to open the modal with details
// Function to open the modal and load details
function openDetailsModal(button) {
    const id = button.getAttribute('data-id');
    const type = button.getAttribute('data-type');

    // Make an AJAX request to fetch the details
    $.ajax({
        url: `/admin_dashboard/${type}_details/${id}`,
        method: 'GET',
        success: function(data) {
            $('#modal-body-adm').html(data);
            $('#details-modal-adm').show();

            // Set button text and action based on current flag status
            const flagButton = document.getElementById('flag-btn-adm');
            const isFlagged = data.includes('Flagged'); // Determine if item is flagged
            flagButton.textContent = isFlagged ? 'Unflag' : 'Flag';
            flagButton.setAttribute('data-id', id);
            flagButton.setAttribute('data-type', type);
        },
        error: function() {
            alert('Failed to load details. Please try again.');
        }
    });
}

function closeDetailsModal() {
    $('#details-modal-adm').hide();
}


// // Optional: Close the modal when clicking outside of it
// $(window).on('click', function(event) {
//     if ($(event.target).is('#details-modal-adm')) {
//         closeDetailsModal();
//     }
// });


function flag(url) {
    window.location.href = url;
}