// Admin Dashboard JavaScript

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.channel-picker').forEach(picker => {
        const search = picker.querySelector('.channel-picker-search');
        const options = picker.querySelectorAll('.channel-picker-option');
        const form = picker.closest('form');
        const error = form.querySelector('.channel-picker-error');

        search.addEventListener('input', function() {
            const query = this.value.trim().toLocaleLowerCase();
            options.forEach(option => {
                option.hidden = !option.dataset.channelName.includes(query);
            });
        });

        form.addEventListener('submit', function(event) {
            const hasSelection = form.querySelector('input[name="channel_ids"]:checked');
            error.hidden = Boolean(hasSelection);
            if (!hasSelection) {
                event.preventDefault();
                search.focus();
            }
        });
    });

    const channelRows = document.querySelectorAll('.filterable-channel');
    const channelSearch = document.getElementById('channelSearch');
    const channelStatusFilter = document.getElementById('channelStatusFilter');
    const channelResultCount = document.getElementById('channelResultCount');
    const channelPageSize = document.getElementById('channelPageSize');
    const eventRows = document.querySelectorAll('.filterable-event');
    const eventSearch = document.getElementById('eventSearch');
    const eventResultCount = document.getElementById('eventResultCount');

    function setupTablePagination(options) {
        let currentPage = 1;

        function update(resetPage = false) {
            if (resetPage) currentPage = 1;

            const query = options.search.value.trim().toLocaleLowerCase();
            const status = options.status ? options.status.value : 'all';
            const matchingRows = Array.from(options.rows).filter(row => {
                const matchesQuery = row.textContent.toLocaleLowerCase().includes(query);
                const matchesStatus = status === 'all' || row.dataset.status === status;
                return matchesQuery && matchesStatus;
            });
            const pageSize = Number(options.pageSize.value);
            const pageCount = Math.max(1, Math.ceil(matchingRows.length / pageSize));
            currentPage = Math.min(currentPage, pageCount);

            const firstRow = (currentPage - 1) * pageSize;
            options.rows.forEach(row => { row.hidden = true; });
            matchingRows.slice(firstRow, firstRow + pageSize).forEach(row => { row.hidden = false; });

            options.resultCount.textContent = `${matchingRows.length} ${options.noun}`;
            options.pageSummary.textContent = `Page ${currentPage} of ${pageCount}`;
            options.previous.disabled = currentPage === 1;
            options.next.disabled = currentPage === pageCount;
            options.pagination.hidden = pageCount <= 1;
            options.emptyState.hidden = options.rows.length === 0 || matchingRows.length > 0;
        }

        options.search.addEventListener('input', () => update(true));
        options.pageSize.addEventListener('change', () => update(true));
        if (options.status) options.status.addEventListener('change', () => update(true));
        options.previous.addEventListener('click', () => {
            currentPage -= 1;
            update();
        });
        options.next.addEventListener('click', () => {
            currentPage += 1;
            update();
        });
        update();
    }

    if (channelSearch && channelStatusFilter && channelResultCount) {
        setupTablePagination({
            rows: channelRows,
            search: channelSearch,
            status: channelStatusFilter,
            resultCount: channelResultCount,
            pageSize: channelPageSize,
            pagination: document.getElementById('channelPagination'),
            pageSummary: document.getElementById('channelPageSummary'),
            previous: document.getElementById('channelPrevious'),
            next: document.getElementById('channelNext'),
            emptyState: document.getElementById('channelNoResults'),
            noun: 'channels'
        });
    }

    if (eventSearch && eventResultCount) {
        setupTablePagination({
            rows: eventRows,
            search: eventSearch,
            pageSize: document.getElementById('eventPageSize'),
            resultCount: eventResultCount,
            pagination: document.getElementById('eventPagination'),
            pageSummary: document.getElementById('eventPageSummary'),
            previous: document.getElementById('eventPrevious'),
            next: document.getElementById('eventNext'),
            emptyState: document.getElementById('eventNoResults'),
            noun: 'events'
        });
    }

    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });
    
    // Confirm delete actions
    const deleteForms = document.querySelectorAll('form[action*="delete"]');
    deleteForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.hasAttribute('data-confirmed')) {
                e.preventDefault();
                if (confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                    form.setAttribute('data-confirmed', 'true');
                    form.submit();
                }
            }
        });
    });
    
    // Stream type helper text
    const streamTypeSelect = document.getElementById('stream_type');
    if (streamTypeSelect) {
        streamTypeSelect.addEventListener('change', function() {
            const streamUrlInput = document.getElementById('stream_url');
            const helpText = streamUrlInput.nextElementSibling;
            
            switch(this.value) {
                case 'm3u8':
                    helpText.textContent = 'Enter HLS stream URL (e.g., https://example.com/stream.m3u8)';
                    break;
                case 'ts':
                    helpText.textContent = 'Enter MPEG-TS stream URL (e.g., https://example.com/stream.ts)';
                    break;
                case 'mp4':
                    helpText.textContent = 'Enter MP4 video URL (e.g., https://example.com/video.mp4)';
                    break;
            }
        });
    }
    
    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.style.borderColor = 'var(--danger-color)';
                } else {
                    field.style.borderColor = 'var(--border-color)';
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                alert('Please fill in all required fields.');
            }
        });
    });
});
