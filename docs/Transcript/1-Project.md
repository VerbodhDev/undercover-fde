

6:01 / 7:47

And now it is my great delight to reveal to you the big project,

the commercial project we'll be working on together throughout the next three weeks,

codenamed UnderCover.

And for the first time in any of my courses,

UnderCover is going to be the same project that we will work

on throughout the next three weeks.

It's going to culminate in a major capstone.

And the reason we're sticking

at one commercial project rather than having three is because we're going

to build it and build it and turn it into something really substantial.

The chunkiest project I've ever built on a course.

Let me tell you what it's all about.

So, UnderCover is a fictional travel insurer,

a company that provides travel insurance.

And that is what we're going to be working on for the next few weeks.

Both the product, the platform, but also an AI agent that's able to process claims.

We're going to cover many aspects of this business.

And maybe you're thinking, insurance?

That doesn't sound particularly juicy.

Believe me, it's gonna be very juicy.

We're gonna build this into something huge.

It's gonna have a real autonomous element to it.

It's gonna be something which we'll be able to take in many different directions,

as you'll see. And it's a big canvas.

There's a lot we can do with this.

It gives us a lot of scope to build that in different directions over the course

of the next three weeks together.

And it's called UnderCover as a bit of a pun, because if you have travel insurance,

then you are under insurance coverage.

Okay, let me tell you what we're about to do.

Throughout building out this project,

we will be playing the role of an AI solutions architect, an FDE,

working with a customer, in this case, the travel insurance customer,

to build out our product, starting with a pilot.

And let me talk you through the brief that we've got

from the UnderCover Claims team about the pilot that we're about to build.

So in our fictional company, UnderCover, today,

there is a team called the Claims Team.

And this team is responsible for looking at a queue of insurance claims

that people have raised.

This is stuff like, I missed my flight because I left the dog at home,

something like that.

And the insurance team, the claims team, sits there, they read each claim,

they review the policies, and they decide whether to approve a policy,

decline a policy, or escalate it for further attention.

And this, today, let's say, is a manual process.

So our pilot, what we're going to be working on initially,

is an AI agent that decides how to process these claims.

It's going to work the queue like one of the members of this claims team.

It's going to look at each decision in turn.

And ideally, it's just going to handle all

of the claims as well as the current handlers do.

It's going to require human approval for any payout more than $1,000,

but less than $1,000, it should be able to handle it itself.

That would be a success.

And with any project like this, before you dig into building out software,

building out an application, you should start by experimenting.

And that's exactly what we're going to do today.

We're going to stick to Jupyter Notebooks, to labs, as we look at the data,

as we try out different LLM calls,

as we understand the kind of quality and cost trade-offs,

and select an LLM for this task by experimenting.

So that's what we'll be doing in a Jupyter Notebook.

So let me talk you through the roadmap of what I have in store for you

for the next three weeks with this project.

And let me assure you that this is going to be the biggest, the boldest,

the most ambitious and enterprise strength of any project I've ever done on any

of my courses.

So if insurance, travel thing sounds pedestrian to you,

it will be anything but pedestrian.

Week one is about becoming an AI engineer.

So we're going to be getting hands-on with this project.

We're going to start today with this notebook work, this experimenting.

Then tomorrow we're going to move to using Claude Code to build out a full back-end,

dashboard front-end and an AI agent.

Then we'll explore open source models.

And then finally bring it home with harness engineering

to build out this agentic AI product.

Then in week two, things get serious.

To go industrial strength with this product, we're gonna add in evals,

observability, we'll explore agentic RAG, memory, some MCP we'll sprinkle in,

we'll have a human in the loop in it, we'll have agent teams,

and we'll have a self-improving, recursive self-improving agent in the mix too.

It's gonna be really exciting.

It's taking it to the next level.

And of course, week three is about taking this to production enterprise caliber.

Security, guardrails, enterprise context layers and integrations and data,

and then deploying using AWS AgentCore and handing over to the client.

That's the final step for an AI FDE as we conclude the capstone project.

Now, there's a few reasons why I chose travel insurance as our setup

for this massive project we'll do together.

And one of them is that it's very tangible.

It's something we all have some experience with, right?

Like, we've all been offered

to take travel insurance by these endless travel websites.

So we know what it's about,

and we've no doubt all had some travel mishaps when we've wished we were insured.

And so this idea of building this out,

it's something that will be meaningful to everyone.

When I've built things like the financial services platforms in past projects,

that won't necessarily resonate with everyone.

But everyone has some experience with travel and insurance.

So this is right in the bullseye.

But more importantly than that, it's a somewhat generic kind of setup.

And what I mean by that is that you could take very similar ideas

that we're going to go through and apply it to so many other businesses.

Any place where you have a kind of operations team that's making a kind

of human-like decision based on some kind of policy framework,

you can think about how far-reaching that is.

But almost any department in any company has something like that going on.

**So it's very easy to imagine how you might take this kind of project and redirect it,**

reshape it, to apply to a different business area,

such as one that you personally have direct experience with.

And so that is my mission for you.

My ask is that you either consider building out this project exactly with me,

going through the steps that I go through.

You can either build at each step and keep going,

or I'm going to give you opportunities to switch over to the version

of code I'm working on at each point.

You can choose how you do that.

But one option is that you just copy me, follow along,

use it as a way to dig in and learn.

But there are some alternatives.

You should consider improving on what I do.

Find ways to add new features.

Find ways to improve on things like security and guardrails and human checks.

Everything we do along the way.

Find ways to do it better than me.

I would love that. And then you should share what you do.

I'll give you a few different ways to do that.

Perhaps contributing it to the repo.

Perhaps posting it on LinkedIn.

And then, of course, if you tag me,

I will weigh in and make sure that I increase the visibility

on what you've built.

But do please look for opportunities to take it further.

Or alternatively, you could take this project and apply it

to a completely different business area.

Perhaps a business area that you've worked in now or in the past

that you know a thing or two about.

Or perhaps it's just a personal pain point,

something that really frustrates you,

where you feel like there's got to be a better way of doing that.

Well, maybe there is, and maybe you'll be the one that builds it.

So please do consider taking what we do and applying it somewhere else.

That will be a really great way to build up your skills.

And then share the code or post about it on LinkedIn and I'll be sure to weigh

in and make sure you get the most visibility possible.
