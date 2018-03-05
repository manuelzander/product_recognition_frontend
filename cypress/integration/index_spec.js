describe('Home page', function() {
    // Visiting our app before each test removes any state build up from
    // previous tests. Visiting acts as if we closed a tab and opened a fresh one
    beforeEach(function () {
        cy.visit('http://127.0.0.1:5000/')
    })

    it('cy.should - assert that the loaded page has correct header', function() {
        // Get the site title and check value
        cy.title().should('include', 'OMEGAP')
    })


    context('Querying', function() {
        it('cy.get() - assert that user can take webcam snapshots', function(){
            // Get the snapshot button and click on it
            cy.get('#snapshot_btn').click()
        })
    })
})

describe('Uploads page', function() {
    // Visiting our app before each test removes any state build up from
    // previous tests. Visiting acts as if we closed a tab and opened a fresh one
    beforeEach(function () {
        cy.visit('http://127.0.0.1:5000/upload')
    })

    it('cy.get - locate the uploads link on menu and navigate', function() {
        // Get the site title and check value
        cy.visit('http://127.0.0.1:5000')
        cy.get('#upload-nav-link').click()
        cy.url().should('eq','http://127.0.0.1:5000/upload')
    })

    context('cy.get - upload an image', function() {
        it('cy.get() - assert that user can upload an image', function(){
            // Get the upload button and click on it
            cy.get('#choose-file').click()
        })
    })
})
