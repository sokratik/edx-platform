class @DiscussionUser
    constructor: (content_info) ->
        @content_info = content_info

    following: (thread) ->
        @content_info[thread.id]['subscribed'] == true

    voted: (thread) ->
        @content_info[thread.id]['voted'] == 'up'

class @ThreadListItemView extends Backbone.View
  tagName: "li"
  template: _.template($("#thread-list-item-template").html())
  initialize: ->
    @model.on "change", @render
  render: =>
    @$el.html(@template(@model.toJSON()))
    @

class @DiscussionThreadListView extends Backbone.View
  render: ->
    @collection.each @renderThreadListItem
  renderThreadListItem: (thread) =>
    view = new ThreadListItemView(model: thread)
    view.render()
    @$el.append(view.el)

class @DiscussionThreadView extends Backbone.View
  events:
    "click .discussion-vote-up": "toggleVote"
    "click .dogear": "toggleFollowing"
  initialize: (options) ->
    @user = options['user']
    @model.bind "change", @updateModelDetails

  updateModelDetails: =>
    @$(".votes-count-number").html(@model.get("votes")["up_count"])

  render: ->
    if @user.following(@model)
      @$(".dogear").addClass("is-followed")

    if @user.voted(@model)
      @$(".vote-btn").addClass("is-cast")

  toggleVote: ->
    @$(".vote-btn").toggleClass("is-cast")
    if @$(".vote-btn").hasClass("is-cast")
      @vote()
    else
      @unvote()

  toggleFollowing: (event) ->
    $elem = $(event.target)
    @$(".dogear").toggleClass("is-followed")
    url = null
    if @$(".dogear").hasClass("is-followed")
      url = @model.urlFor("follow")
    else
      url = @model.urlFor("unfollow")
    DiscussionUtil.safeAjax
      $elem: $elem
      url: url
      type: "POST"

  vote: ->
    url = @model.urlFor("upvote")
    @$(".votes-count-number").html(parseInt(@$(".votes-count-number").html()) + 1)
    DiscussionUtil.safeAjax
      $elem: @$(".discussion-vote")
      url: url
      type: "POST"
      success: (response, textStatus) =>
        if textStatus == 'success'
          @model.set(response)

  unvote: ->
    url = @model.urlFor("unvote")
    @$(".votes-count-number").html(parseInt(@$(".votes-count-number").html()) - 1)
    DiscussionUtil.safeAjax
      $elem: @$(".discussion-vote")
      url: url
      type: "POST"
      success: (response, textStatus) =>
        if textStatus == 'success'
          @model.set(response)

$ ->
  window.$$contents = {}
  window.$$discussions = {}
