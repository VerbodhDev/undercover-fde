

3:54 / 13:52

Welcome to the create_agent part of the lab.

This is what it's all been leading up to.

So far, we've been making single LLM calls using structured outputs.

Now we're going to use a different approach, an AI agent.

It's going to be an LLM with tools in a loop to achieve a goal.

And we're going to be using this create_agent framework in LangChain,

this create_agent function,

which allows us to do some of the general boilerplate code for us,

making it easier to use an agent.

So here's how it works.

We're going to first describe an LLM call using a class like ChatOpenAI,

one of the abstraction classes in LangChain.

We're then going to turn some functions into tools using the @tool decorator,

and then create_agent, and then invoke.

That is the power function in LangChain to do anything.

All right, let's start with a very, very simple example.

First of all, just very vanilla LangChain to make a simple LLM call.

All right, so with LangChain, you start by creating this object, ChatOpenAI.

We're going to tell it the model we use.

I'll use openrouter/free for this quick example.

That's the base URL.

That's the API key for OpenRouter that we created up above from the .env file.

We set up a messages list of dictionaries exactly the same way as before.

A helpful assistant who answers, in the style of a pirate,

what's the meaning of the universe.

And then if we want to call this LLM, everything in LangChain,

when you want to do something, it's always invoke.

So we say, let's take this LLM, let's invoke it with these messages,

and we'll print back what it says.

That's how easy it is to use LangChain.

And here you have Arr, me hearties.

That'd be a question as vast as the ocean itself.

That is what we get back from a free model on OpenRouter,

calling it via LangChain's abstraction classes.

Okay, now I'm going to create a little dictionary called recorded

that we're going to use to track everything that we record.

And then I've got two functions here, get_policy and record_decision.

get_policy, which looks up a customer's policy record,

the actual policy that the customer has purchased.

record_decision, which records the response from an LLM by shoving it

in this recorded dictionary.

And it's just going to add it in in claim_id and record that decision.

So these are just two normal Python functions.

But I've put these little decorators, @tool, before them.

And just by decorating it with @tool,

the LangChain framework will automatically turn these into things

that could be called by an LLM.

It will describe it with some JSON without us having to worry about the JSON.

And with that, we are going to say, okay, let's have Luna again.

ChatOpenAI. We give it the model GPT-6 Luna.

The OpenRouter base URL, the key.

We want low reasoning effort.

And now we're going to have our system prompt and our user prompt.

The system prompt is to use your tools to look up the customer's policy record

and record your decision.

That is the full policy wording going in there.

The user prompt, there we are going to say, this is the claim right here.

But what we're not doing, we did before,

before we put the customer's policy in here too.

We're not putting that in here.

We're going to ask the agent to retrieve that policy.

That's one of the tools that we're giving it.

So that is the system prompt and the user prompt.

Very similar to before.

Except we're not putting the customer's policy in here in the user prompt.

And now, this is where it comes together.

We use create_agent, the function from LangChain.

We give it the model, Luna, which we just created up here.

We give it the tools, get_policy and record_decision.

These are the two tools that we just defined and a couple

of cells up there with the @tool, or just one cell up here, right here.

**With this @tool decorator right here, these two tools,**

we can just pass them in to create_agent, just like that.

And we give it a system prompt right here.

And now, we have done our create_agent.

That means we now have an agent.

All that's left to do is to run that agent.

I wonder how we'd run the agent.

Yes, I know you know well.

We run the agent the way you run everything in LangChain,

by calling invoke. We call invoke.

We pass in the message of this claim.

All right, off it goes.

We are calling our AI agent, which has now been equipped with two tools.

It's going to use its tools.

It's done it all already.

It all happened. So it used its tool calls to get a policy.

That was the policy it got back.

And then it recorded, based on that, that it wanted to approve.

It approved for $420.

And you probably remember that is indeed the correct answer.

We just ran an agent in a loop with tools to achieve a goal.

It achieved the goal.

It got it right. That is LangChain's create_agent at work.

And now just as before we're going to have like a decide function.

This time it's decide_with_agent that's going to go through and time it

and run it and record what happens.

And so that is what I'm going to kick off now.

This is now going to run the 25 data points just as before and it's going

to call agent.invoke as it does it and then return this little dictionary.

And we're going to here go through for claim in claims.

This is where we loop through the 25.

For each one, we call decide_with_agent for that particular claim.

And I will see you in a second when this completes, and we'll see how it does.

All right, it completed.

It took a minute and 55 seconds.

25 of 25 claims have a recorded decision.

Let's take a look at the results.

So, if we compare the LLM with the agent, the LLM got 18 right,

the agent got 17 right,

and you can see the agent did cost a fair bit more because it had to do

that various tool callings.

So there was a little bit more work in there,

and it also took a fair bit longer because it had to do that as well.

So, actually, when I last ran this, they got exactly the same results.

So I'm sure this is just noise.

They do tend to get basically the same results.

I hope you got the same results, too, but I'm not going to cherry pick this.

I'll stick with this, but I would put that down to the normal noise.

The bottom line is

that the agent approach over structured output does take a little bit longer

and costs a little bit more.

And if you want to dig in,

you can look at the ones that they missed and have a look to see what happened.

I'd be interested to see what kind of results you get,

whether you get the same as this or whether they are identical

or whether one tends to do better than the other.

And I'm just going to finish it with a quick summary table.

Here it is. This shows you the different approaches that we used.

If we compare the different reasonings as well, all of them used LLM calls,

except the last one was agent.

When it came to accuracy, the winner was GPT-6 Luna as an LLM call.

It did fractionally worse as an agent, but I think that's just noise.

I would ignore that.

I would say it's been a dead heat most of the time I've run it.

And then we got a better result from GPT-6 Sol.

We got more accurate, less accurate with Flash Lite.

When it comes to cost, of course, as you can probably imagine,

it was most expensive with Sol.

And then it was quite expensive using Gemini Flash Lite.

And then it becomes successively cheaper to use Luna as an agent,

Luna on medium and Luna on low with a direct LLM call.

And when it comes to time,

the agent was the slowest of all because it had

to navigate through those tool calls.

So some very interesting data here for you to explore.

But hopefully you're trying more.

Try more models. Run this a few times.

Experiment with different models.

See what you can discover in terms of the accuracy,

cost and speed of the different techniques and the different models

and reasoning levels.

Now, I know what you're thinking.

You're thinking, okay, Ed, but hang on a second.

Hang on right there.

You're telling me, you're telling me, if you're that kind of type, you say,

you're telling me, you're telling me that the agent solution,

when using the same model, basically took longer, was more expensive,

and in this case, a little bit worse, and I did try it twice,

it was worse both times, worse than just using Luna alone.

So what's the point in using an agent?

Is that what you're telling me?

And if so, what's the answer?

What's the answer to that?

Can you answer that challenge yourself?

And the answer is that in this specific situation,

it makes no sense to use an agent because the benefit that you get

with an AI agent is you're introducing the idea of autonomy.

You're allowing the LLM to choose to use different tools,

to choose to perhaps explore the data, to run different queries,

to use its judgment, which is anthropomorphizing,

but using the tokens that it predicts to allow it to decide whether

or not it should use one tool or another.

But in this case,

that was somewhat fake because we always wanted it to use the tool

to get the customer's policy and then to use the tool to record its decision.

We had a fixed workflow.

And so getting that,

sort of crowbarring that into an agent isn't a good use of agent functionality.

We were introducing autonomy where it's not really needed and it's not beneficial.

And as a result, it took longer because it had to do all these tool calls.

And in fact, it turns out it seems to have done a worse job in this case,

for whatever reason.

Perhaps we just got lucky with that call that I made to Luna before.

But that makes you think agents should not always be the right answer.

Use agents where you need that extra power and flexibility that comes

with allowing an LLM to choose the workflow.

Allowing an LLM to decide which tools to use and why based on the problem at hand.

And just because we're trying to use this to replicate a human agent,

an insurance agent, doesn't mean that an AI agent is the right solution.

An agent is not always the right solution.

And you might be thinking, okay,

then why did you choose this example and why are we going through

and building agents?

And hopefully you got the answer to that one as well.

Do you have the answer?

The answer is because we're just getting started.

And you already saw from this problem with the manual cases that we might need

to provide it with more information.

And in fact,

giving it access to more information and allowing it to have autonomy to be able

to decide what to do.

Whilst that might take a bit longer and

in some situations be a bit more pricey than having a fixed workflow,

a simple LLM call with structured outputs.

Maybe it'll be a bit harder, but it will allow us to do more.

It would allow us to equip the agent with more tools and eventually

to get much more accurate results.

And that is the whole point.

And that's what we'll be coming to in the coming days.

And so, to the assignment for you.

There will always be assignments throughout this.

This is what I'd like to ask you to do,

and this is the best way to build true expertise.

Go through this lab and experiment with different models and different approaches.

Use the agent approach, maybe add on some new tools.

Try and find,

if you can get a solution that gets

at least 15 correct consistently using the agent

and find the cheapest model you can do that with.

And see what you can come up with, and then let me know.

I want to know what solution you come up with.

I want to know the lowest price point, maybe free,

that you can do and get at least 15 right.

And if you get 15, then see if you get 16.

See how much you can get accurate at a very low price point.

That is the challenge for you.

And when you've done that, please consider submitting that as some code,

your version of this with your results.

And then if you could make a PR,

you could post that so that I can include it in community contributions.

You make a PR, if you're not familiar with the process for making a PR,

I've got a link here that gives you instructions.

It's a way that you can use GitHub to send me a version of the code,

which is then only included in this community contributions folder,

so it doesn't change this main lab.

And then I will accept it.

And as a result, you'll have contributed to this repo, which is really cool.

So you'll be one of the contributors to the repo.

You'll also be able to see your code in here and you'll see other students

that have done this.

You'll see their versions of the lab here in community contributions.

Such a great way to be involved in this repo and to see other solutions.

How cheap can you go?

How accurate can you get?

Put it in as a PR.

And when you've done that, you should consider making a post on LinkedIn.

If you wish, say something about what you learned, your takeaways,

something about how you discovered more about the trade-offs between accuracy

and speed and cost,

and perhaps what your solution was and your main takeaways or insights from it.

And if you tag me on that and mention it's from this lab, then of course,

I'll come on in. I will weigh in.

I will add some comments to help amplify your achievement

and make sure you get the most visibility.

So please take me up on that.

Go and do that.

And again, if you see that I've done that for another student on this course,

then please jump in yourself, weigh in, and amplify their success.

It's a great way to support the community.

And that, at last, is a wrap on week one, day two.

And look, I feel a bit guilty that I had suggested earlier that maybe day two

was going to be shorter than day one, and it ended up being a bit longer, I think.

But I feel like it was worth it, because it's really got everyone on the same page.

Maybe you already knew most of this, in which case, hopefully,

some useful revision, and then I threw in Jev,

a couple of other things here and there.

And if you didn't know it, it may have been a bit of a trial by fire, as I say,

but hopefully you're now up to speed.

And if not, remember, there are those other courses, too.

OK,

congratulations. Week one, day two, is behind you.

You're already 13% of the way through the course.

We're just getting warmed up.

Get ready for day three on Coding Agents.

So much ahead. See you then
