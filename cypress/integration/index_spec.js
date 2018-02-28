describe('Uploads page', function() {
    beforeEach(function () {})

    it('cy.should - assert that <title> is correct', function() {
        // Get the site title and check value
        cy.visit('http://127.0.0.1:5000/upload')
        cy.title().should('include', 'OMEGAP')
    })


    context('Querying', function() {
        it('cy.get() - query DOM elements', function(){
            // Get the upload buttons and click on them
            cy.get('#upload').find('#single-upload').click()
            cy.get('#upload').find('#multiple-upload').click()
        })
    })
})

describe('Home page', function() {
    beforeEach(function () {})

    it('cy.should - assert that <title> is correct', function() {
        // Get the site title and check value
        cy.visit('http://127.0.0.1:5000/')
        cy.title().should('include', 'OMEGAP')
    })


    context('Querying', function() {
        it('cy.get() - query DOM elements', function(){
            // Get the snapshot buttons and click on them
            // cy.get('#upload').find('#single-upload').click()
            // cy.get('#upload').find('#multiple-upload').click()
            // test change
            // see if pre-receive hooks runs tests
        })
    })
})