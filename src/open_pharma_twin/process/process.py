from .compartments import factory

# Process Modell
def campaignA(env, runID, plant: factory):  # Process Control
    yield env.process(upstream(env, runID, plant))


def upstream(env, runID, plant):
    # Stage 1
    ## Init
    active_vessel_stage1 = plant.ferm_stage1.get_vessel()
    yield active_vessel_stage1.activate_resource()

    ## prod1
    start_time = env.now
    yield env.process(active_vessel_stage1.produce(runID))
    end_time_s1 = env.now

    # Stage 2
    active_vessel_stage2 = plant.ferm_stage2.get_vessel()
    yield active_vessel_stage2.activate_resource()
    active_vessel_stage1.release_resource()

    start_time_s2 = env.now
    yield env.process(active_vessel_stage2.produce(runID))
    end_time_s2 = env.now

    # Stage 3
    active_vessel_stage3 = plant.ferm_stage3.get_vessel()
    yield active_vessel_stage3.activate_resource()
    active_vessel_stage2.release_resource()

    start_time_s3 = env.now
    yield env.process(active_vessel_stage3.produce(runID))
    end_time_s3 = env.now

    # Stage 4
    active_vessel_stage4 = plant.ferm_stage4.get_vessel()
    yield active_vessel_stage4.activate_resource()
    active_vessel_stage3.release_resource()

    start_time_s4 = env.now
    yield env.process(active_vessel_stage4.produce(runID))
    end_time_s4 = env.now

    # Harvest
    active_harvester = plant.harvester.get_vessel()
    yield active_harvester.activate_resource()
    active_vessel_stage4.release_resource()

    start_time_h = env.now
    yield env.process(active_harvester.produce(runID))
    end_time_h = env.now
    active_harvester.release_resource()

    # Post Analysis
    end_time = env.now
    duration = end_time - start_time
    duration_s1 = end_time_s1 - start_time
    duration_s2 = end_time_s2 - start_time_s2
    duration_s3 = end_time_s3 - start_time_s3
    duration_s4 = end_time_s4 - start_time_s4
    duration_h = end_time_h - start_time_h

    res_dict = {
        "run": runID, "campaign_type": "CampaignA", "campaign_duration": duration,
        "start_campaign": start_time, "end_campaign": end_time, "duration_campaign": duration,
        "stage1_start": start_time, "stage1_end": end_time_s1, "stage1_duration": duration_s1,
        "stage2_start": start_time_s2, "stage2_end": end_time_s2, "stage2_duration": duration_s2,
        "stage3_start": start_time_s3, "stage3_end": end_time_s3, "stage3_duration": duration_s3,
        "stage4_start": start_time_s4, "stage4_end": end_time_s4, "stage4_duration": duration_s4,
        "harvest_start": start_time_h, "harvest_end": end_time_h, "harvest_duration": duration_h,
    }
    env.prod_durations.append(res_dict)

