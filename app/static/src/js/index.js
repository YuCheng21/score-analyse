$(document).ready(function () {
    // console.log('ready')

})

/**
 * manualModal
 */
$('#manualModal').on('hide.bs.modal', function () {
    $('video').each(function () {
        this.pause();
        this.currentTime = 0;
    });
})

/**
 * singleCert
 */
$('#singleCertInput').change(function () {
    $('#singleCert').submit()

    const loading = $('<div class="loading">Loading&#8230;</div>');
    $('body').prepend(loading);
})

/**
 * signInModal
 */
$('#signInSend').click(function () {
    $('#signInForm').submit()
})

$('#signInForm .username, #signInForm .password').keypress(function (e) {
    const KEY_ENTER = 13
    if (e.which === KEY_ENTER) {
        $('#signInForm').submit()
    }
})

$('#signInModal').on('hide.bs.modal', function () {
    $('#signInForm .username, #signInForm .password').val('')
})

/**
 * signUpModal
 */
$('#signUpSend').click(function () {
    $('#signUpForm').submit()
})

$('#signUpForm .username, #signUpForm .password').keypress(function (e) {
    const KEY_ENTER = 13
    if (e.which === KEY_ENTER) {
        $('#signUpForm').submit()
    }
})

/**
 * changeInfoModal
 */
$('#changeInfoSend').click(function () {
    changeInfo()
})

$('#changeInfoForm .password, #changeInfoForm .passwordConfirm').keypress(function (e) {
    const KEY_ENTER = 13
    if (e.which === KEY_ENTER) {
        changeInfo()
    }
})

function changeInfo() {
    const password = $('#changeInfoForm #password')
    const passwordConfirm = $('#changeInfoForm #passwordConfirm')
    if (password.val() != "" && password.val() === passwordConfirm.val()) {
        $('#changeInfoForm').submit()
    } else {
        password.addClass('is-invalid')
        passwordConfirm.addClass('is-invalid')
    }
}

$('#changeInfoModal').on('hide.bs.modal', function () {
    $('#changeInfoForm .password, #changeInfoForm .passwordConfirm').val('')
})

/**
 * passedTableModal
 */
$('#passedTableSend').click(function () {
    $('#passedTableForm').submit()

})

$('#passedTableModal').on('hide.bs.modal', function () {
    $('#passedTableModal .passedTableInput').val('')
})

/**
 * multipleCertModal
 */
$('#multipleCertSend').click(function () {
    var formData = new FormData(document.querySelector('#multipleCertForm'))
    const loading = $('<div class="loading">Loading&#8230;</div>');
    $('body').prepend(loading);

    axios({
        url: url_multiple_cert,
        method: "POST",
        data: formData,
        responseType: "arraybuffer",
        onUploadProgress(progressEvt) {
            var percentCompleted = Math.round((progressEvt.loaded * 100) / progressEvt.total)
            // console.log(percentCompleted)
        },
        onDownloadProgress(progressEvt) {
            var percentCompleted = Math.round((progressEvt.loaded * 100) / progressEvt.total)
            // console.log(percentCompleted)
        },
    }).then(function (res) {
        // console.log(res)
        var blob = new Blob([res.data], {type: "octet/stream"});
        const disposition = res.headers['content-disposition']
        const keyword = 'filename='
        const start = disposition.indexOf(keyword) + keyword.length
        const filename = disposition.substring(start)
        saveAs(blob, filename);
    }).catch(function (err) {
        console.log(err)
    }).finally(function () {
        // console.log('finally')
        loading.remove()
    })
})

$('#multipleCertModal').on('hide.bs.modal', function () {
    $('#multipleCertModal .multipleCertInput, #multipleCertModal .serialNumber').val('')
})

